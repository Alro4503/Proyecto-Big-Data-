# Análisis de Precios de Vivienda en California

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/BigQuery-SQL-orange?logo=google-cloud&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?logo=powerbi&logoColor=black)
![Orange](https://img.shields.io/badge/Orange-Data%20Mining-orange)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker&logoColor=white)
![Licencia](https://img.shields.io/badge/Licencia-CC0%20Public%20Domain-lightgrey)
![Metodología](https://img.shields.io/badge/Metodología-CRISP--DM-green)

---

## Tabla de contenidos

- [Abstract](#abstract)
- [Introducción](#introducción)
- [Desarrollo](#desarrollo)
- [Resultados](#resultados)
- [Conclusiones](#conclusiones)
- [Bibliografía](#bibliografía)
- [Estructura del proyecto](#estructura-del-proyecto)

---

## Abstract

Análisis del dataset California Housing (censo de 1990) aplicando la metodología CRISP-DM. El dataset recoge datos de 20.640 bloques censales del estado de California e incluye variables socioeconómicas, demográficas y geográficas. El objetivo es determinar qué factores influyen en el precio mediano de la vivienda a nivel de bloque censal. Se utilizan Python para el análisis exploratorio y la limpieza, BigQuery para consultas analíticas, Orange Data Mining para modelado supervisado y Power BI para la visualización. El ingreso mediano del bloque resulta ser el predictor más relevante (r = 0,688), y el modelo Random Forest obtiene un R² de 0,797 en validación cruzada de 10 pliegues.

---

## Introducción

El mercado inmobiliario californiano acumula décadas de tensión entre oferta y demanda, con precios que varían enormemente según la zona. Estudiar los factores detrás de esas diferencias tiene utilidad tanto para el análisis económico como para decisiones de planificación urbana o inversión.

El dataset utilizado proviene del censo de California de 1990 y fue publicado por Pace, R. Kelley y Ronald Barry (1997). Cada fila representa un **bloque censal** — la unidad geográfica mínima del censo americano — no una vivienda individual. Esto tiene implicaciones importantes: `total_rooms`, `total_bedrooms`, `population` y `households` son totales del bloque entero, no de una sola vivienda.

**Variables del dataset:**

| Variable               | Descripción                                              |
|------------------------|----------------------------------------------------------|
| `longitude`            | Longitud geográfica del bloque censal                    |
| `latitude`             | Latitud geográfica del bloque censal                     |
| `housing_median_age`   | Edad mediana de las viviendas del bloque (años)          |
| `total_rooms`          | Total de habitaciones en el bloque censal                |
| `total_bedrooms`       | Total de dormitorios en el bloque (207 nulos)            |
| `population`           | Población total del bloque censal                        |
| `households`           | Número de hogares en el bloque censal                    |
| `median_income`        | Ingreso mediano del bloque (en decenas de miles de USD)  |
| `median_house_value`   | Precio mediano de vivienda en USD — variable objetivo    |
| `ocean_proximity`      | Proximidad al océano (5 categorías)                      |

Dos particularidades del dataset que afectan al análisis: `median_income` no está en USD directos sino en decenas de miles (un valor de 3,87 equivale a 38.700 USD reales), y `median_house_value` tiene un techo artificial en 500.001 USD impuesto durante la recogida del censo.

---

## Desarrollo

### Herramientas

| Herramienta           | Uso                                                             |
|-----------------------|-----------------------------------------------------------------|
| Python 3.11           | Análisis exploratorio, limpieza, visualización, estandarización |
| BigQuery SQL          | Consultas analíticas sobre la tabla del proyecto                |
| Orange Data Mining    | Regresión lineal, árbol de decisión y Random Forest             |
| Power BI Desktop      | Dashboard interactivo con mapas, KPIs y filtros                 |
| Docker / Compose      | Entorno reproducible para ejecutar el script de análisis        |

### Ejecución

**Con Docker:**
```bash
git clone <repo-url>
cd Proyecto-Big-Data-
docker-compose up --build
```

**En local:**
```bash
cd python
pip install -r requirements.txt
python analisis.py
```

Los gráficos se generan en `graficos/` y el CSV procesado en `data/housing_clean.csv`.

### Metodología CRISP-DM

1. **Comprensión del negocio** — definir qué factores determinan el precio de la vivienda en California.
2. **Comprensión de los datos** — exploración de dimensiones, tipos, distribuciones y valores nulos.
3. **Preparación de los datos** — imputación de 207 nulos en `total_bedrooms` con la mediana, creación de variables derivadas por hogar, eliminación de atípicos extremos en `population_per_household`, one-hot encoding de `ocean_proximity` y estandarización z-score.
4. **Modelado** — regresión lineal, árbol de regresión y Random Forest evaluados con validación cruzada de 10 pliegues en Orange Data Mining.
5. **Evaluación** — comparativa de R², RMSE y MAE entre los tres modelos.
6. **Despliegue** — dashboard en Power BI, consultas en BigQuery y script ejecutable con Docker.

---

## Resultados

### Correlaciones con el precio

| Variable                   | r       |
|----------------------------|---------|
| `median_income`            | **+0,688** |
| `rooms_per_household`      | +0,151  |
| `housing_median_age`       | +0,106  |
| `bedrooms_per_room`        | -0,259  |
| `population_per_household` | -0,023  |

### Precio mediano por proximidad al océano

| Categoría   | Precio mediano (USD) |
|-------------|---------------------|
| ISLAND      | ~380.000            |
| NEAR BAY    | ~258.000            |
| NEAR OCEAN  | ~243.000            |
| \<1H OCEAN  | ~240.000            |
| INLAND      | ~119.000            |

### Gráficos generados por el script

| Archivo                                    | Contenido                                  |
|--------------------------------------------|--------------------------------------------|
| `graficos/01_histograma_precios.png`       | Distribución del precio mediano            |
| `graficos/02_scatter_ingresos_precio.png`  | Ingreso mediano vs precio de vivienda      |
| `graficos/03_boxplot_ocean_proximity.png`  | Precios por categoría de proximidad        |
| `graficos/04_heatmap_correlaciones.png`    | Mapa de correlaciones entre variables      |
| `graficos/05_mapa_geoespacial.png`         | Distribución geográfica de precios         |

### Comparativa de modelos (CV 10-fold, Orange Data Mining)

| Modelo             | R²    | RMSE (USD) | MAE (USD) |
|--------------------|-------|-----------|----------|
| Regresión lineal   | 0,657 | 67.509    | 48.678   |
| Árbol de regresión | 0,666 | 66.545    | 43.383   |
| Random Forest      | **0,797** | **51.910** | **34.149** |

---

## Conclusiones

1. **El ingreso del bloque censal es el factor más determinante del precio.** Con una correlación de r = 0,688, `median_income` explica por sí solo más variabilidad en el precio que el resto de variables combinadas. La desigualdad económica se refleja directamente en el mercado inmobiliario.

2. **Vivir cerca del océano tiene un precio.** Los bloques `ISLAND` y `NEAR BAY` tienen precios medianos más de tres veces superiores a los bloques del interior (`INLAND`). La localización geográfica introduce una prima que las variables socioeconómicas no capturan por sí solas.

3. **El techo de 500.001 USD distorsiona el extremo superior de la distribución.** Alrededor del 7 % de los bloques alcanzan ese valor máximo artificial, lo que comprime la cola derecha y puede sesgar al alza los modelos de regresión en ese rango.

4. **Las variables de tamaño del bloque están multicolineadas.** `total_rooms`, `total_bedrooms`, `households` y `population` contienen información muy solapada. Las variables derivadas por hogar (`rooms_per_household`, `bedrooms_per_room`) son más informativas porque normalizan esa redundancia.

5. **Los precios altos se concentran geográficamente.** El mapa muestra clústeres claros en el Área de la Bahía de San Francisco y la cuenca de Los Ángeles, lo que confirma que latitud y longitud son predictores útiles y que los modelos espaciales podrían mejorar los resultados obtenidos.

---

## Bibliografía

- Pace, R. Kelley & Ronald Barry (1997). *Sparse Spatial Autoregressions*. Statistics & Probability Letters, 33(3), 291-297.
- Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3.ª ed.). O'Reilly Media.
- Kaggle California Housing Prices Dataset. Licencia CC0 Public Domain. [https://www.kaggle.com/datasets/camnugent/california-housing-prices](https://www.kaggle.com/datasets/camnugent/california-housing-prices)
- Chapman, P. et al. (2000). *CRISP-DM 1.0: Step-by-step data mining guide*. SPSS Inc.
- McKinney, W. (2022). *Python for Data Analysis* (3.ª ed.). O'Reilly Media.

---

## Estructura del proyecto

```
Proyecto-Big-Data-/
├── data/
│   ├── housing.csv
│   └── housing_clean.csv
├── graficos/
│   ├── 01_histograma_precios.png
│   ├── 02_scatter_ingresos_precio.png
│   ├── 03_boxplot_ocean_proximity.png
│   ├── 04_heatmap_correlaciones.png
│   └── 05_mapa_geoespacial.png
├── python/
│   ├── analisis.py
│   ├── requirements.txt
│   └── Dockerfile
├── sql/
│   └── queries.sql
├── orange/
│   └── README_orange.md
├── powerbi/
│   └── README_powerbi.md
├── docs/
│   └── README_docs.md
├── docker-compose.yml
└── README.md
```
