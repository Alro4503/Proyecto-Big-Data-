# Orange Data Mining – Pipeline de Análisis

## Descripción

Orange Data Mining es una herramienta visual de análisis de datos que permite construir flujos de trabajo arrastrando y soltando componentes (*widgets*). En este proyecto se utiliza para aplicar modelos de regresión supervisada sobre el dataset California Housing y comparar su rendimiento.

## Dataset de entrada

Utilizar el archivo `data/housing_clean.csv` generado por el script `python/analisis.py`.

- **Separador de columna:** punto y coma (`;`)
- **Separador decimal:** coma (`,`)
- **Variable objetivo:** `median_house_value`
- **Tipo de problema:** regresión (variable continua)

## Pipeline de widgets

```
[File]
   │
   ▼
[Select Columns]
   │  Target:  median_house_value
   │  Features: median_income, housing_median_age, total_rooms,
   │            total_bedrooms, population, households,
   │            rooms_per_household, bedrooms_per_room,
   │            population_per_household, longitude, latitude
   │  Ignorar: columnas _z (estandarizadas) y one-hot ocean_*
   │
   ▼
[Data Sampler] ─────────────────────────────────────────┐
   │  Estrategia: Fixed proportion                      │
   │  Train: 80 %  |  Test: 20 %  (semilla = 42)       │
   │                                                    │
   ▼                                                    ▼
[Linear Regression]   [Regression Tree]   [Random Forest]
   │  Ridge λ = 0,001   │  Max depth = 10   │  Árboles = 100
   │                    │                   │  Max features = √n
   └──────────┬─────────┘                   │
              │                             │
              └─────────────────────────────┘
                          │
                          ▼
                   [Test and Score]
                      │  Validación cruzada 10-fold
                      │  Métricas: R², RMSE, MAE, MAPE
                      │
                      ▼
                 [Predictions]
```

## Configuración paso a paso

### 1. File
- Abrir Orange y arrastrar el widget **File** al lienzo.
- Seleccionar `data/housing_clean.csv`.
- Configurar: separador `;`, decimal `,`, primera fila como cabecera.

### 2. Select Columns
- Conectar **File → Select Columns**.
- Mover `median_house_value` a *Target*.
- Mover las columnas numéricas de interés a *Features*.
- Excluir columnas `_z` (ya estandarizadas) y las columnas `ocean_*` (one-hot, ya incorporado en la variable original si se prefiere trabajar con la versión sin OHE).

### 3. Data Sampler
- Conectar **Select Columns → Data Sampler**.
- Estrategia: *Fixed proportion of data* → 80 %.
- Activar *Reproducible sampling* con semilla 42.
- Salidas: *Data Sample* (train) y *Remaining Data* (test).

### 4. Modelos
Arrastrar tres widgets de regresión y conectar cada uno a **Data Sampler (Data Sample)**:
- **Linear Regression**: usar regularización Ridge, λ = 0,001.
- **Regression Tree**: profundidad máxima = 10.
- **Random Forest Regression**: 100 árboles, *Max features* = √n\_features.

### 5. Test and Score
- Conectar **Data Sampler → Test and Score** (como datos de prueba).
- Conectar los tres modelos → **Test and Score**.
- Seleccionar *Cross Validation*, 10 pliegues.
- Métricas visibles: **R²**, **RMSE**, **MAE**.

### 6. Predictions
- Conectar **Test and Score → Predictions** para ver las predicciones individuales frente a los valores reales.

## Resultados esperados (referencia)

| Modelo               | R²    | RMSE (USD) | MAE (USD) |
|----------------------|-------|-----------|----------|
| Linear Regression    | ~0,64 | ~67.000   | ~49.000  |
| Regression Tree      | ~0,62 | ~69.000   | ~45.000  |
| Random Forest        | ~0,81 | ~50.000   | ~35.000  |

> Los valores son aproximados. El Random Forest supera a los otros dos modelos gracias al ensamblado de árboles que reduce la varianza.

## Interpretación

- **R² ~ 0,81** (Random Forest): el modelo explica el 81 % de la variabilidad en el precio mediano de vivienda.
- **RMSE ~ 50.000 USD**: el error típico de predicción es de ±50.000 USD por bloque censal.
- La variable más influyente es `median_income`, coherente con la correlación de Pearson r = 0,688 observada en el análisis exploratorio.

## Exportar resultados
- Desde **Test and Score**: botón *Save* → exportar tabla de métricas como CSV.
- Desde **Predictions**: conectar un widget **Data Table** y exportar desde ahí.
