import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
from utils import BaseStrategy

data = pd.read_parquet('data.parquet')
if data.index.tz is not None:
    data.index = data.index.tz_localize(None)
data['date'] = data.index.date

class StrategyQuality(BaseStrategy):
    def __init__(self, data, window_days=5, top_k=5):
        df = data.copy()
        df['date'] = df.index.date
        super().__init__(df)
        self.cash = self.capital
        self.window = window_days
        self.k = top_k

    def before_open(self, day) -> dict:
        if hasattr(day, 'tzinfo') and day.tzinfo is not None:
            day = day.tz_localize(None)

        hist = self.data[self.data['date'] < day.date()]
        if hist.empty:
            return {'selected': []}

        recent = hist.loc[hist.index >= (day - pd.Timedelta(days=self.window + 2))]
        if recent.empty:
            return {'selected': []}

        df = recent.copy()
        df['date'] = df.index.date
        daily = df.groupby(['symbol', 'date']).agg(
            open=('price', 'first'),
            close=('price', 'last'),
            volatility=('price', 'std'),
            volume=('size', 'sum'),
            bid=('bid_px_00', 'mean'),
            ask=('ask_px_00', 'mean')
        ).reset_index()
        daily['spread'] = (daily['ask'] - daily['bid']) / daily['open']
        daily['return'] = daily['close'] / daily['open'] - 1

        qf = (daily.groupby('symbol')
              .agg({'spread': 'mean', 'volume': 'mean', 'volatility': 'mean', 'return': 'mean'})
              .dropna())

        qf['spread_score'] = -qf['spread'].rank()
        qf['volume_score'] = qf['volume'].rank()
        med = qf['volatility'].median()
        qf['volatility_score'] = (-abs(qf['volatility'] - med)).rank()
        qf['quality_score'] = (0.9 * qf['volatility_score'] +
                               0.6 * qf['spread_score'] +
                               0.1 * qf['volume_score'])

        today_syms = set(self.data[self.data['date'] == day.date()]['symbol'])
        qf = qf.loc[qf.index.isin(today_syms)]
        if qf.empty:
            return {'selected': list(today_syms)[:self.k]}

        sel = qf.sort_values('quality_score', ascending=False).head(self.k).index.tolist()
        return {'selected': sel}

    def trading_session(self, day, params) -> None:
        sel = params.get('selected', [])
        if not sel:
            return

        today = self.data[self.data['date'] == day.date()]
        if today.empty:
            return

        held = self.qts[self.qts != 0].index.tolist()
        for sym in held:
            if sym not in sel:
                df_sym = today[today.symbol == sym]
                if not df_sym.empty:
                    ft = df_sym.iloc[0]
                    self.trade(ft.name, sym, 'NYSE', ft.price, self.qts[sym], 'SELL')

        cash_each = self.cash / len(sel)
        for sym in sel:
            df_sym = today[today.symbol == sym]
            if not df_sym.empty:
                ft = df_sym.iloc[0]
                qty = cash_each / ft.price
                if qty > 0:
                    self.trade(ft.name, sym, 'NYSE', ft.price, qty, 'BUY')

    def after_close(self, day) -> float:
        today = self.data[self.data['date'] == day.date()]
        closes = today.groupby('symbol').price.last()
        closes = closes.reindex(self.qts.index).fillna(0)
        nav = self.cash + (self.qts * closes).sum()
        return nav

# Definimos rango de fechas 
start = datetime(2023, 3, 28)
end   = datetime(2023, 12, 29)

strategy = StrategyQuality(data, window_days=5, top_k=5)

all_days    = sorted(data['date'].unique())
trading_days = [pd.to_datetime(d) for d in all_days if start <= pd.to_datetime(d) <= end]

pnl, idx = [], []
for day in trading_days:
    params = strategy.before_open(day)
    strategy.trading_session(day, params)
    pnl.append(strategy.after_close(day))
    idx.append(day)
strategy.pnl_history = pd.Series(pnl, index=idx)

def calculate_sharpe_and_cvar(strat):
    eq    = strat.pnl_history.ffill()
    daily = eq.diff().dropna()
    if daily.std() == 0:
        print("Equity plano: Sharpe/CVaR no disponibles")
        return np.nan, np.nan
    sharpe = np.sqrt(252) * daily.mean() / daily.std()
    var95  = daily.quantile(0.05)
    cvar95 = daily[daily <= var95].mean()
    print(f"Sharpe Ratio: {sharpe:.4f}   CVaR(95%): {cvar95:.2f}")
    return sharpe, cvar95

sharpe, cvar = calculate_sharpe_and_cvar(strategy)


eq = strategy.pnl_history.ffill()
fig = px.line(eq,
              title="Equity Curve (NAV)",
              labels={'index': 'Fecha', 'value': 'Capital ($)'},
              template='plotly_white')
fig.update_layout(showlegend=False)
fig.show()


from IPython.display import display
td = strategy.trade_monitor.trades
print(f"\nTotal operaciones: {len(td)}")
display(td.head(10))
