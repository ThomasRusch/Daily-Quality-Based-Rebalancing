**Estrategia de Rebalanceo Quality con Backtesting Adaptativo Diario**
Descripción de la Estrategia


Se utiliza un enfoque de rebalanceo diario basado en la selección de los top 5 activos con mejor "Quality Score", calculado a partir de factores de calidad de mercado como volatilidad, spread y volumen.

La estrategia parte de la hipótesis de que activos con mejores propiedades de liquidez y estabilidad tienden a mostrar un desempeño más consistente y favorable.

⚙️ Construcción del Quality Score

Para lograr esto, se extraen y promedian diariamente los siguientes factores para cada activo:

Volatilidad intradía (se favorecen valores bajos)
Spread relativo (se favorecen niveles eficientes)
Volumen transado (se favorecen valores altos)

Luego, los activos se rankean y se construye el score de la siguiente forma:

```python
quality_score = 0.90 * volatility_score  # promueve estabilidad
               + 0.60 * spread_score     # promueve eficiencia
               + 0.10 * volume_score     # asegura liquidez
```

Esta combinación busca maximizar la rentabilidad ajustada por riesgo, evitando drawdowns pronunciados.

###Lógica de Inversión

La estrategia incorpora un proceso de adaptación diaria:

- Se seleccionan los top 5 activos con mayor quality_score cada día
- Se utiliza una ventana de 5 días + 2 días de cobertura
- Si un activo sale del ranking:
- Se liquida la posición
- El capital se redistribuye en partes iguales entre los nuevos seleccionados

Esto permite mantener una cartera dinámica y alineada con las mejores condiciones de mercado.

###Resultados

Con los datos entregados y la estrategia implementada, se obtuvieron los siguientes resultados:

- Sharpe Ratio: 1.7453
- CVaR: -24.106,70

Estos resultados muestran:

- Crecimiento sostenido
- Riesgo controlado
- Ausencia de drawdowns excesivos

Todo esto gracias al uso de factores de calidad como filtro de inversión.

###Instrucciones del Proyecto

Las instrucciones completas para el desarrollo de este proyecto se encuentran en el archivo Proyecto Final.pdf, incluido en este repositorio.

En dicho documento se detallan:

- El objetivo del proyecto
- La descripción del dataset
- La estructura del código
- Las restricciones de implementación
- Las métricas de evaluación

Se recomienda revisarlo para entender completamente el contexto del desarrollo.

###Datos

El dataset (data.parquet) no está incluido en este repositorio debido a restricciones de tamaño.

Estructura:

├── analysis.ipynb   # Exploratory analysis & strategy development
├── main.py          # Final strategy implementation
├── utils.py         # Base classes (Strategy, TradeMonitor)
├── data.parquet     # Input dataset
└── README.md        # Project documentation

Para ejecutar el proyecto:

1. Obtener el dataset entregado durante el curso
2. Ubicarlo en la carpeta raíz del proyecto: /data.parquet
3. Cargarlo utilizando:

3. Load it using:

```python
import pandas as pd
df = pd.read_parquet("data.parquet")
```

🧪 Reproducibilidad

La estrategia es completamente reproducible siempre que se tenga acceso al dataset.

Todo el preprocesamiento, la construcción de variables (feature engineering) y la lógica de trading están implementados en:

analysis.ipynb
main.py

Si quieres, el siguiente paso sería dejarlo aún más competitivo para CV (estilo JPM / BTG / hedge fund) con una versión más corta tipo executive summary.
