Estrategia de Rebalanceo Quality con Backtesting Adaptativo Diario

Se utiliza un enfoque de rebalanceo diario basado en la selección de los top 5 activos con mejor "Quality Score", calculado a partir de factores de de calidad de mercado como volatilidad, spread y volumen. Esta estrategia parte de la hipótesis de que activos con mejores propiedades de liquidez y estabilidad tienden a revertir positivamente su desempeño.

Para lograr ello, se extraen y promedian diariamente los siguientes factores para cada activo:
- Volatilidad intradía (baja)
- Spread relativo (medio)
- Volumen transado (alto)

De ahí rankeados los activos, se pondera la cartera por las siguientes ponderaciones:
quality_score = 0.90 * volatility_score (promueve estabilidad)
               + 0.60 * spread_score (promueve eficiencia)
               + 0.10 * volume_score (asegura liquidez)

Esta combinación busca maximizar la rentabilidad ajustada por riesgo, evitando drawdowns pronunciados.

Importante recalcar que se hace un proceso de adaptación diaria, en donde se escogen el top 5 de activos con mayor quality_score entre los disponibles ese día dentro del rango de 5 días más dos de cobertura. Si en ese plazo los activos se escapan del top se liquidan y se reparte el capital en partes iguales entre los nuevos seleccionados. 

Finalmente con los datos entregados y la estrategia utilizada, se logró obtener un ratio de Sharpe de 1,7453 y un Cvar de -24.106,70, mostrando un crecimiento sostenido, sin drawdowns excesivos, gracias al uso de factores de calidad como filtro.


######################

## 📦 Data

The dataset (`data.parquet`) is not included in this repository due to size constraints.

To run the project:
1. Obtain the dataset provided during the course
2. Place it in the root folder of the project: /data.parquet
3. 3. Load it using:

```python
import pandas as pd
df = pd.read_parquet("data.parquet")

## 🧪 Reproducibility

The strategy is fully reproducible given access to the dataset. 
All preprocessing, feature engineering, and trading logic are implemented in `analysis.ipynb` and `main.py`.

