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

Este proyecto aplica la metodología CRISP-DM al dataset California Housing (1990), que contiene 20.640 bloques censales del estado de California con variables socioeconómicas y geográficas. El objetivo es identificar los factores que determinan el precio mediano de la vivienda a nivel de bloque censal. El análisis combina estadística descriptiva en Python, consultas analíticas en BigQuery, modelado supervisado en Orange Data Mining y visualización interactiva en Power BI. El ingreso mediano del bloque censal es el predictor más fuerte (r = 0,688), y el modelo Random Forest alcanza un R² de aproximadamente 0,81 en validación cruzada.

---

## Introducción

El mercado inmobiliario californiano es uno de los más dinámicos y desiguales de Estados Unidos. Comprender qué factores determinan los precios de la vivienda es fundamental para decisiones de política pública, inversión inmobiliaria y análisis socioeconómico.

El dataset California Housing fue recopilado del censo de California de 1990 y publicado por Pace, R. Kelley y Ronald Barry (1997). Cada registro representa un **bloque censal** — la unidad geográfica más pequeña del censo — y no una vivienda individual. Las variables `total_rooms`, `total_bedrooms`, `population` y `households` son agregados del bloque completo.

**Características del dataset:**

| Variable               | Descripción                                              |
|------------------------|----------------------------------------------------------|
| `longitude`            | Longitud geográfica del bloque censal                    |
| `latitude`             | Latitud geográfica del bloque censal                     |
| `housing_median_age`   | Edad mediana de las viviendas del bloque (años)          |
| `total_rooms`          | Total de habitaciones en el bloque censal                |
| `total_bedrooms`       | Total de dormitorios en el bloque (207 nulos)            |
| `population`           | Población total del bloque censal                        |
| `households`           | Número de hogares en el bloque censal                    |
| `median_income`        | Ingreso mediano del bloque (decenas de miles USD)        |
| `median_house_value`   | **Variable objetivo** – precio mediano USD (techo 500K) |
| `ocean_proximity`      | Proximidad al océano (5 categorías)                      |

> **Nota importante:** `median_income` = 3,87 equivale a 38.700 USD reales. El valor máximo registrado de `median_house_value` es 500.001 USD, que corresponde a un techo artificial impuesto durante la recogida del censo.

---

## Desarrollo

### Herramientas utilizadas

| Herramienta           | Uso en el proyecto                                              |
|-----------------------|-----------------------------------------------------------------|
| Python 3.11           | Análisis exploratorio, limpieza, visualización, estandarización |
| BigQuery SQL          | Consultas analíticas a escala sobre la tabla del proyecto       |
| Orange Data Mining    | Modelado supervisado (Linear Regression, Tree, Random Forest)   |
| Power BI Desktop      | Dashboard interactivo con mapas, KPIs y slicers                 |
| Docker / Compose      | Entorno reproducible para ejecutar el script Python             |

### Ejecución con Docker

```bash
# 1. Clonar el repositorio y colocar housing.csv en data/
git clone <repo-url>
cp housing.csv data/

# 2. Construir y ejecutar el contenedor
docker-compose up --build

# 3. Los gráficos aparecerán en graficos/ y el CSV limpio en data/housing_clean.csv
```

### Ejecución local (sin Docker)

```bash
cd python
pip install -r requirements.txt
python analisis.py
```

### Metodología CRISP-DM

1. **Comprensión del negocio** – Identificar los factores de precio en el mercado inmobiliario californiano.
2. **Comprensión de los datos** – Exploración del dataset: dimensiones, tipos, nulos, estadísticas descriptivas.
3. **Preparación de los datos** – Imputación de 207 nulos en `total_bedrooms` (mediana), creación de variables derivadas, eliminación de atípicos en `population_per_household`, one-hot encoding y estandarización z-score.
4. **Modelado** – Regresión lineal, árbol de regresión y Random Forest en Orange Data Mining con validación cruzada 10-fold.
5. **Evaluación** – Comparativa de R², RMSE y MAE entre los tres modelos.
6. **Despliegue** – Dashboard Power BI, consultas BigQuery, script Docker-compatible.

---

## Resultados

### Análisis de correlaciones

| Variable                  | Correlación con precio (r) |
|---------------------------|---------------------------|
| `median_income`           | **+0,688**                |
| `rooms_per_household`     | +0,151                    |
| `housing_median_age`      | +0,106                    |
| `bedrooms_per_room`       | -0,259                    |
| `population_per_household`| -0,023                    |

### Precio mediano por proximidad al océano

| Categoría       | Precio mediano (USD) |
|-----------------|---------------------|
| ISLAND          | ~380.000            |
| NEAR BAY        | ~258.000            |
| NEAR OCEAN      | ~243.000            |
| <1H OCEAN       | ~240.000            |
| INLAND          | ~119.000            |

### Gráficos generados

Los siguientes gráficos son producidos automáticamente por `python/analisis.py`:

| Gráfico                              | Archivo                              |
|--------------------------------------|--------------------------------------|
| Histograma de precios                | `graficos/01_histograma_precios.png` |
| Scatter ingreso vs precio            | `graficos/02_scatter_ingresos_precio.png` |
| Boxplots por ocean_proximity         | `graficos/03_boxplot_ocean_proximity.png` |
| Heatmap de correlaciones             | `graficos/04_heatmap_correlaciones.png` |
| Mapa geoespacial de California       | `graficos/05_mapa_geoespacial.png` |

### Comparativa de modelos (Orange Data Mining, CV 10-fold)

| Modelo               | R²    | RMSE (USD) | MAE (USD) |
|----------------------|-------|-----------|----------|
| Regresión lineal     | ~0,64 | ~67.000   | ~49.000  |
| Árbol de regresión   | ~0,62 | ~69.000   | ~45.000  |
| Random Forest        | ~0,81 | ~50.000   | ~35.000  |

---

## Conclusiones

1. **El ingreso mediano es el determinante principal del precio.** Con r = 0,688, `median_income` explica individualmente más variabilidad en el precio que cualquier otra variable del dataset. Las políticas habitacionales que ignoren la desigualdad de ingresos subestiman el problema.

2. **La proximidad al océano genera una prima de precio sustancial.** Los bloques de categoría `ISLAND` y `NEAR BAY` tienen precios medianos hasta tres veces superiores a los bloques `INLAND`. La localización geográfica es un factor no capturado por las variables socioeconómicas.

3. **El techo artificial de 500.001 USD distorsiona el análisis.** Aproximadamente el 7 % de los bloques alcanzan este valor máximo, lo que comprime artificialmente la distribución y puede sesgar los modelos de regresión al alza en el extremo superior.

4. **Existe multicolinealidad entre las variables de tamaño del bloque.** `total_rooms`, `total_bedrooms`, `households` y `population` están altamente correlacionadas entre sí. Las variables derivadas (`rooms_per_household`, `bedrooms_per_room`) son mejores predictores al normalizar por número de hogares.

5. **Los clústeres geográficos de precios coinciden con áreas metropolitanas.** El mapa geoespacial revela concentraciones de precio alto en el Área de la Bahía de San Francisco y la cuenca de Los Ángeles, lo que sugiere que la variable de localización (latitud/longitud) puede usarse directamente como predictor en modelos espaciales.

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
│   ├── .gitkeep               # Carpeta rastreada en git (sin el CSV)
│   ├── housing.csv            # Dataset original (NO incluido en git)
│   └── housing_clean.csv      # Generado por analisis.py (NO incluido en git)
├── graficos/
│   ├── .gitkeep               # Carpeta rastreada en git
│   ├── 01_histograma_precios.png
│   ├── 02_scatter_ingresos_precio.png
│   ├── 03_boxplot_ocean_proximity.png
│   ├── 04_heatmap_correlaciones.png
│   └── 05_mapa_geoespacial.png
├── python/
│   ├── analisis.py            # Script principal de análisis
│   ├── requirements.txt       # Dependencias Python
│   └── Dockerfile             # Imagen Docker para el script
├── docker-compose.yml         # Orquestación Docker con volúmenes
├── sql/
│   └── queries.sql            # 7 consultas BigQuery comentadas
├── orange/
│   └── README_orange.md       # Pipeline y configuración de Orange
├── powerbi/
│   └── README_powerbi.md      # Dashboard y medidas DAX
├── docs/
│   └── README_docs.md         # Índice de documentación
└── README.md                  # Este archivo
```
