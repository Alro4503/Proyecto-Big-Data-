# Orange Data Mining

El archivo `orange_bigdata.ows` contiene el flujo de trabajo de modelado supervisado sobre el dataset California Housing. Se comparan tres modelos de regresión para predecir el precio mediano de vivienda por bloque censal.

## Modelos y configuración

| Modelo             | Configuración                        |
|--------------------|--------------------------------------|
| Linear Regression  | Regularización Ridge, λ = 0,001      |
| Regression Tree    | Profundidad máxima = 10              |
| Random Forest      | 100 árboles, max features = √n       |

Validación: cross-validation de 10 pliegues. Variable objetivo: `median_house_value`.

## Resultados

| Modelo             | R²    | RMSE (USD) | MAE (USD) |
|--------------------|-------|-----------|----------|
| Linear Regression  | 0,657 | 67.509    | 48.678   |
| Regression Tree    | 0,666 | 66.545    | 43.383   |
| Random Forest      | 0,797 | 51.910    | 34.149   |

El Random Forest es significativamente mejor que los otros dos (p < 0,001). Explica casi el 80 % de la variabilidad en el precio, con un error típico de ±52.000 USD por bloque censal. La variable con mayor peso es `median_income`, consistente con la correlación de r = 0,688 del análisis exploratorio.
