# Análisis de Precios de Vivienda en California

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
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
  - [Herramientas](#herramientas)
  - [Fase 1 — Comprensión del negocio](#fase-1--comprensión-del-negocio)
  - [Fase 2 — Comprensión de los datos](#fase-2--comprensión-de-los-datos)
  - [Fase 3 — Preparación de los datos](#fase-3--preparación-de-los-datos)
  - [Fase 4 — Modelado](#fase-4--modelado)
  - [Fase 5 — Evaluación](#fase-5--evaluación)
  - [Fase 6 — Despliegue](#fase-6--despliegue)
- [Resultados](#resultados)
- [Conclusiones](#conclusiones)
- [Bibliografía](#bibliografía)
- [Anexos](#anexos)
- [Estructura del proyecto](#estructura-del-proyecto)

---

## Abstract

Análisis del dataset California Housing (censo de 1990) aplicando la metodología CRISP-DM. El dataset recoge datos de 20.640 bloques censales del estado de California e incluye variables socioeconómicas, demográficas y geográficas. El objetivo es determinar qué factores influyen en el precio mediano de la vivienda a nivel de bloque censal. Se utilizan Python para el análisis exploratorio y la limpieza, Orange Data Mining para el modelado supervisado y Power BI para la visualización. El ingreso mediano del bloque resulta ser el predictor más relevante (r = 0,688), y el modelo Random Forest obtiene un R² de 0,797 en validación cruzada de 10 pliegues.

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

Dos particularidades del dataset afectan al análisis: `median_income` no está en USD directos sino en decenas de miles (un valor de 3,87 equivale a 38.700 USD reales), y `median_house_value` tiene un techo artificial en 500.001 USD impuesto durante la recogida del censo.

---

## Desarrollo

### Herramientas

| Herramienta           | Uso                                                             |
|-----------------------|-----------------------------------------------------------------|
| Python 3.11           | Análisis exploratorio, limpieza, visualización, estandarización |
| Orange Data Mining    | Regresión lineal, árbol de decisión y Random Forest             |
| Power BI Desktop      | Dashboard interactivo con mapas, KPIs y filtros                 |
| Docker / Compose      | Entorno reproducible para ejecutar el script de análisis        |

**Ejecución del script Python:**

```bash
# Con Docker
git clone <repo-url>
cd Proyecto-Big-Data-
docker-compose up --build

# En local
cd python
pip install -r requirements.txt
python analisis.py
```

Los gráficos se generan en `graficos/` y el CSV procesado en `data/housing_clean.csv`.

---

### Fase 1 — Comprensión del negocio

**Pregunta de negocio:** ¿Qué variables socioeconómicas, demográficas y geográficas determinan el precio mediano de la vivienda en los bloques censales de California?

**Objetivo analítico:** construir modelos de regresión que permitan estimar `median_house_value` a partir del resto de variables, e identificar cuáles de ellas tienen mayor capacidad predictiva.

**Restricciones identificadas al inicio:**
- El dataset es de 1990; los precios absolutos no son extrapolables al mercado actual, pero los patrones relacionales sí son válidos como ejercicio de análisis.
- La variable objetivo tiene un techo artificial en 500.001 USD que habrá que tener en cuenta durante la evaluación de modelos.

---

### Fase 2 — Comprensión de los datos

El dataset tiene **20.640 filas** y **10 columnas** (9 numéricas + 1 categórica).

**Exploración inicial con Python:**

```python
df.shape        # (20640, 10)
df.dtypes       # float64 x9, object x1
df.isnull().sum()
# total_bedrooms    207  ← único campo con nulos (1,0 % del total)
```

**Distribuciones relevantes:**
- `median_house_value` presenta sesgo positivo moderado con un pico artificial en 500.001 USD.
- `median_income` tiene una distribución aproximadamente log-normal, lo que justifica su alta correlación con el precio.
- `population` y `total_rooms` muestran colas muy largas con valores extremos (máx. 35.682 personas en un bloque).

**Hallazgo clave:** existe multicolinealidad fuerte entre `total_rooms`, `total_bedrooms`, `households` y `population` (todas miden tamaño del bloque). Las variables derivadas por hogar son más informativas.

---

### Fase 3 — Preparación de los datos

Las transformaciones se aplicaron en este orden dentro de `python/analisis.py`:

1. **Imputación de nulos** — los 207 valores faltantes en `total_bedrooms` se reemplazaron con la mediana (433,0). Se eligió la mediana sobre la media por la presencia de outliers en esa variable.

2. **Creación de variables derivadas:**
   ```python
   df['rooms_per_household']      = df['total_rooms']    / df['households']
   df['bedrooms_per_room']        = df['total_bedrooms'] / df['total_rooms']
   df['population_per_household'] = df['population']     / df['households']
   ```

3. **Eliminación de outliers extremos** — se filtraron los bloques con `population_per_household` > 6 (bloques institucionales o errores de datos, menos del 0,5 % del total).

4. **One-hot encoding** de `ocean_proximity` (5 categorías → 4 columnas dummy, se descarta una para evitar multicolinealidad perfecta).

5. **Estandarización z-score** de las variables numéricas continuas para el modelo de regresión lineal:
   ```python
   from sklearn.preprocessing import StandardScaler
   scaler = StandardScaler()
   df_scaled = scaler.fit_transform(df_numeric)
   ```

El dataset limpio se exportó a `data/housing_clean.csv` (20.422 filas tras eliminar outliers extremos).

---

### Fase 4 — Modelado

Se construyó un flujo de trabajo en Orange Data Mining con tres modelos evaluados mediante **validación cruzada estratificada de 10 pliegues**:

- **Regresión lineal** — modelo base, asume relación lineal entre predictores y variable objetivo.
- **Árbol de regresión** — captura relaciones no lineales; profundidad máxima limitada a 7 para evitar sobreajuste.
- **Random Forest** — conjunto de 100 árboles con muestreo aleatorio de variables en cada nodo; parámetro `min_samples_leaf = 5`.

---

### Fase 5 — Evaluación

| Modelo             | R²        | RMSE (USD) | MAE (USD) |
|--------------------|-----------|------------|-----------|
| Regresión lineal   | 0,657     | 67.509     | 48.678    |
| Árbol de regresión | 0,666     | 66.545     | 43.383    |
| Random Forest      | **0,797** | **51.910** | **34.149**|

**Interpretación:**
- El salto de R² entre regresión lineal (0,657) y Random Forest (0,797) indica que hay relaciones no lineales relevantes que la regresión no captura.
- Un MAE de 34.149 USD sobre precios que oscilan entre 15.000 y 500.001 USD supone un error medio del ~7 %, aceptable para datos de 1990 sin variables externas como tasas de interés o índices de criminalidad.
- La brecha entre árbol individual y Random Forest confirma el efecto beneficioso del ensamblado: la varianza se reduce al promediar 100 árboles.

---

### Fase 6 — Despliegue

Los productos finales del proyecto son:

| Producto                              | Descripción                                              |
|---------------------------------------|----------------------------------------------------------|
| `data/housing_clean.csv`              | Dataset limpio y listo para reutilizar                   |
| `graficos/*.png`                      | 5 gráficos de análisis exploratorio generados por Python |
| `orange/orange_bigdata.ows`           | Flujo de Orange reproducible con los tres modelos        |
| `powerbi/ProyectoHousingBigData.pbix` | Dashboard interactivo con mapas, KPIs y filtros          |
| `docker-compose.yml`                  | Entorno reproducible para ejecutar el script             |

---

## Resultados

### Correlaciones con el precio

| Variable                   | r de Pearson |
|----------------------------|-------------|
| `median_income`            | **+0,688**  |
| `rooms_per_household`      | +0,151      |
| `housing_median_age`       | +0,106      |
| `bedrooms_per_room`        | -0,259      |
| `population_per_household` | -0,023      |

### Precio mediano por proximidad al océano

| Categoría   | Precio mediano (USD) |
|-------------|---------------------|
| ISLAND      | ~380.000            |
| NEAR BAY    | ~258.000            |
| NEAR OCEAN  | ~243.000            |
| \<1H OCEAN  | ~240.000            |
| INLAND      | ~119.000            |

### Comparativa de modelos (CV 10-fold, Orange Data Mining)

| Modelo             | R²        | RMSE (USD) | MAE (USD) |
|--------------------|-----------|------------|-----------|
| Regresión lineal   | 0,657     | 67.509     | 48.678    |
| Árbol de regresión | 0,666     | 66.545     | 43.383    |
| Random Forest      | **0,797** | **51.910** | **34.149**|

---

## Conclusiones

1. **El ingreso del bloque censal es el factor más determinante del precio.** Con una correlación de r = 0,688, `median_income` explica por sí solo más variabilidad en el precio que el resto de variables combinadas. La desigualdad económica se refleja directamente en el mercado inmobiliario.

2. **Vivir cerca del océano tiene un precio.** Los bloques `ISLAND` y `NEAR BAY` tienen precios medianos más de tres veces superiores a los bloques del interior (`INLAND`). La localización geográfica introduce una prima que las variables socioeconómicas no capturan por sí solas.

3. **El techo de 500.001 USD distorsiona el extremo superior de la distribución.** Alrededor del 7 % de los bloques alcanzan ese valor máximo artificial, lo que comprime la cola derecha y puede sesgar al alza los modelos de regresión en ese rango.

4. **Las variables de tamaño del bloque están multicolineadas.** `total_rooms`, `total_bedrooms`, `households` y `population` contienen información muy solapada. Las variables derivadas por hogar (`rooms_per_household`, `bedrooms_per_room`) son más informativas porque normalizan esa redundancia.

5. **Los precios altos se concentran geográficamente.** El mapa muestra clústeres claros en el Área de la Bahía de San Francisco y la cuenca de Los Ángeles, lo que confirma que latitud y longitud son predictores útiles y que los modelos espaciales podrían mejorar los resultados obtenidos.

---

## Bibliografía

### Fuentes académicas y técnicas

- Pace, R. Kelley & Ronald Barry (1997). *Sparse Spatial Autoregressions*. Statistics & Probability Letters, 33(3), 291-297.
- Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3.ª ed.). O'Reilly Media.
- Chapman, P. et al. (2000). *CRISP-DM 1.0: Step-by-step data mining guide*. SPSS Inc.
- McKinney, W. (2022). *Python for Data Analysis* (3.ª ed.). O'Reilly Media.
- Demšar, J. et al. (2013). *Orange: Data Mining Toolbox in Python*. Journal of Machine Learning Research, 14, 2349-2353.

### Fuentes de datos y documentación

- Kaggle California Housing Prices Dataset. Licencia CC0 Public Domain. [https://www.kaggle.com/datasets/camnugent/california-housing-prices](https://www.kaggle.com/datasets/camnugent/california-housing-prices)
- Microsoft (2024). *Power BI documentation*. [https://learn.microsoft.com/power-bi/](https://learn.microsoft.com/power-bi/)

### Herramientas de inteligencia artificial utilizadas

Durante el desarrollo de este proyecto se utilizaron herramientas de IA generativa como apoyo en las siguientes tareas:

| Herramienta        | Uso                                                                              |
|--------------------|----------------------------------------------------------------------------------|
| Claude (Anthropic) | Asistencia en la revisión y estructuración del código Python y la documentación  |

El uso de estas herramientas se limitó a soporte en la redacción de código, revisión de calidad y organización de la documentación. Todo el análisis, las decisiones metodológicas y las conclusiones son propias del autor.

---

## Anexos

### Gráficos generados por Python

| Histograma de precios | Scatter ingreso vs precio |
|---|---|
| ![Histograma de distribución del precio mediano de vivienda en California](graficos/01_histograma_precios.png) | ![Dispersión entre ingreso mediano y precio de vivienda](graficos/02_scatter_ingresos_precio.png) |

| Boxplot por proximidad al océano | Mapa de calor de correlaciones |
|---|---|
| ![Boxplot de precios por categoría de proximidad al océano](graficos/03_boxplot_ocean_proximity.png) | ![Mapa de calor de correlaciones entre variables](graficos/04_heatmap_correlaciones.png) |

![Mapa geoespacial de distribución de precios en California](graficos/05_mapa_geoespacial.png)

---

### Flujo de trabajo — Orange Data Mining

![Flujo de trabajo en Orange Data Mining con los tres modelos de regresión](orange/orange_workflow.png)

### Resultados de modelos — Orange Test and Score

![Tabla de resultados de los tres modelos en Orange Test and Score](orange/orange_results.png)

---

### Dashboard — Power BI

![Dashboard interactivo de Power BI con mapas, KPIs y filtros por categoría](powerbi/PowerBI_Dashboard.png)

---

## Estructura del proyecto

```
Proyecto-Big-Data-/
├── data/
│   ├── housing.csv                  ← dataset original (CC0)
│   └── housing_clean.csv            ← generado por analisis.py
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
├── orange/
│   ├── orange_bigdata.ows
│   ├── orange_workflow.png
│   └── orange_results.png
├── powerbi/
│   ├── ProyectoHousingBigData.pbix
│   └── PowerBI_Dashboard.png
├── docs/
│   └── README_docs.md
├── docker-compose.yml
└── README.md
```
