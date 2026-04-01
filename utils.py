import numpy as np
import pandas as pd
from datetime import datetime

class TradeMonitor:
    def __init__(self):
        self.trades = pd.DataFrame(columns = ('time', 'symbol', 'exchange', 'price', 'qty', 'side'))

    def log(self, trade: dict):
        """
        Append to trades df
        """
        self.trades  = pd.concat([self.trades, pd.DataFrame([trade])], ignore_index = True)

    def show(self):
        """
        Returns a styled df with green/red colors for corresponding side (BUY/SELL)
        """
        def colorize(row):
            if row['side'] == 'BUY':
                return ['background-color: rgb(76, 153, 0)'] * len(row)
            elif row['side'] == 'SELL':
                return ['background-color: rgb(204, 0, 10)'] * len(row)
            else:
                return [''] * len(row)
            
        return self.trades.style.apply(colorize, axis=1)


class BaseStrategy:
    def __init__(self, data: pd.DataFrame):
        self.data: pd.DataFrame = data
        self.qts: pd.Series = pd.Series(0, index = data.symbol.unique())
        self.cash: float = 0
        self.capital: float = 500_000 
        self.trade_monitor = TradeMonitor()

    def backtest(self, start: datetime, end: datetime) -> None:
        """ 
        Backtest strategy looping trough all business days
        """
        dates = pd.bdate_range(start, end)
        pnl_history = pd.Series(None, dtype = np.float32, index = dates)
        for day in dates:
            try:
                pnl = self.daily_backtest(day)
            except Exception:
                print('Backtesting Error!')
            else:
                pnl_history[day] = pnl

        self.pnl_history = pnl_history

    def daily_backtest(self, day: datetime) -> float:
        """
        Backtest a single day. 
        If you need something from a method, you can return it.
        Ex: Return estimated parameters in the before_open method and use them in the trading session
        """
        pnl = None
        try:
            params: dict = self.before_open(day)
            self.trading_session(day, params)
            daily_pnl = self.after_close(day)
            
        except Exception as e:
            print(f'Error on {day.date()}: {e}')

        return daily_pnl
        
    def before_open(self, 
                    day: datetime):
        pass

    def trading_session(self, 
                        day: datetime, 
                        params: dict):
        pass

    def after_close(self, day) -> float:
        """
        Get Cumulative PnL marked to market with today close prices
        """
        #Get close prices of each symbol to mark to market 
        today_data = self.data[self.data.index.date == day.date()]
        close_prices = today_data.groupby('symbol').price.last()
        pnl = self.cash + self.qts@close_prices
        return pnl

    def trade(self, t: datetime, symbol: str, exchange: str, 
              price: float, qty: float, side: str) -> None:
        """
        Acts as market trade with Fill rate 100%
        qty: Domain R+
        """
        assert qty >= 0, 'qty must be a positive value.'
        assert price > 0, 'price must be a positive value.'

        if side == 'BUY':
            self.cash -= price*qty
            self.qts[symbol] = self.qts.get(symbol, 0) + qty
        elif side == 'SELL':
            self.cash += price*qty
            self.qts[symbol] = self.qts.get(symbol, 0) - qty

        self.trade_monitor.log(
            {
                'time': t, 
                'symbol': symbol,
                'exchange': exchange,
                'price': price,
                'qty': qty,
                'side': side}
            )
        

    def performance(self) -> dict:
        """
        Calculate metrics based on daily_pnls.
        """
        self.equity_curve = self.pnl_history + self.capital
        daily_pnls = self.equity_curve.ffill().diff()

        sharpe_ratio = np.sqrt(252)*daily_pnls.mean()/daily_pnls.std()
        var_95 = daily_pnls.quantile(95)
        cvar_95 = daily_pnls[daily_pnls <= var_95].mean()
        
        return {'Sharpe': sharpe_ratio,
                'CVar': cvar_95} 

 


