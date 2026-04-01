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

El dataset (data.parquet) no está incluido en este repositorio debido a restricciones de tamaño.

Para ejecutar el proyecto:

1. Obtener el dataset entregado durante el curso
2. Ubicarlo en la carpeta raíz del proyecto: /data.parquet
3. Cargarlo utilizando:
   
import pandas as pd
df = pd.read_parquet("data.parquet")


##Reproducibilidad

La estrategia es completamente reproducible siempre que se tenga acceso al dataset.
Todo el preprocesamiento, la construcción de variables (feature engineering) y la lógica de trading están implementados en analysis.ipynb y main.py.

