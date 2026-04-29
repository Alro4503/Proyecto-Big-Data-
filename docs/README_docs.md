# Documentación del Proyecto

Esta carpeta contiene los documentos de soporte del análisis de datos de California Housing.

## Contenido

| Archivo                          | Descripción                                                          |
|----------------------------------|----------------------------------------------------------------------|
| `informe_final.pdf`              | Informe completo del proyecto siguiendo la metodología CRISP-DM      |
| `presentacion.pdf`               | Diapositivas de la presentación del proyecto                         |
| `graficos/`                      | Copia de los gráficos generados por el script de Python              |

> Los gráficos generados automáticamente se guardan en la carpeta raíz `graficos/`. Esta carpeta contiene únicamente copias manuales o versiones exportadas para el informe.

## Gráficos generados

Los siguientes gráficos son generados por `python/analisis.py` y guardados en `graficos/`:

| Archivo                           | Descripción                                          |
|-----------------------------------|------------------------------------------------------|
| `01_histograma_precios.png`       | Distribución del precio mediano de vivienda          |
| `02_scatter_ingresos_precio.png`  | Correlación ingreso mediano vs precio de vivienda    |
| `03_boxplot_ocean_proximity.png`  | Comparativa de precios por proximidad al océano      |
| `04_heatmap_correlaciones.png`    | Mapa de calor de correlaciones entre variables       |
| `05_mapa_geoespacial.png`         | Distribución geográfica de precios en California     |

## Estructura de la documentación (CRISP-DM)

El informe final sigue las seis fases de la metodología CRISP-DM:

1. **Comprensión del negocio** – Contexto del mercado inmobiliario californiano y objetivo del análisis.
2. **Comprensión de los datos** – Descripción del dataset: 20.640 bloques censales, 10 variables, 207 nulos.
3. **Preparación de los datos** – Imputación de nulos, variables derivadas, eliminación de atípicos, one-hot encoding y estandarización z-score.
4. **Modelado** – Regresión lineal, árbol de regresión y Random Forest evaluados con validación cruzada 10-fold en Orange Data Mining.
5. **Evaluación** – Comparativa de R², RMSE y MAE. El Random Forest obtiene el mejor R² (~0,81).
6. **Despliegue** – Dashboard en Power BI, consultas en BigQuery, script Docker-compatible para reproducibilidad.

## Hallazgos clave

- La variable con mayor correlación con el precio es `median_income` (r = 0,688).
- Los precios están artificialmente truncados en 500.001 USD (7 % de los bloques alcanzan este techo).
- Los bloques costeros (`ISLAND`, `NEAR BAY`) presentan precios hasta tres veces superiores a los del interior (`INLAND`).
- Existe multicolinealidad entre `total_rooms`, `total_bedrooms`, `households` y `population`.
- Los clústeres geográficos de precios altos coinciden con el Área de la Bahía de San Francisco y Los Ángeles.
