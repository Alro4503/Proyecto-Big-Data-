# Power BI – Dashboard California Housing

## Descripción

Este documento describe el diseño del dashboard interactivo de Power BI para el análisis de precios de vivienda en California. El informe se construye sobre el archivo `data/housing_clean.csv` generado por el script de análisis.

## Conexión de datos

1. Abrir Power BI Desktop.
2. **Obtener datos → Texto o CSV**.
3. Seleccionar `data/housing_clean.csv`.
4. En el paso de *Transformar datos* (Power Query):
   - Delimitor: punto y coma (`;`)
   - Separador decimal: coma (`,`)
   - Establecer tipo **Número decimal** en todas las columnas numéricas.
   - Establecer tipo **Texto** en las columnas `ocean_*` (o reconstruir `ocean_proximity` si se importa el CSV original).
5. Cerrar y aplicar.

## Modelo de datos

Tabla única: **housing_clean**

| Columna                    | Tipo       | Descripción                               |
|----------------------------|------------|-------------------------------------------|
| longitude / latitude       | Decimal    | Coordenadas del bloque censal             |
| housing_median_age         | Decimal    | Edad mediana de las viviendas             |
| total_rooms                | Decimal    | Total de habitaciones en el bloque        |
| total_bedrooms             | Decimal    | Total de dormitorios en el bloque         |
| population                 | Decimal    | Población del bloque censal               |
| households                 | Entero     | Número de hogares                         |
| median_income              | Decimal    | Ingreso mediano (decenas de miles USD)    |
| median_house_value         | Decimal    | **Variable objetivo** – precio en USD     |
| rooms_per_household        | Decimal    | Variable derivada                         |
| bedrooms_per_room          | Decimal    | Variable derivada                         |
| population_per_household   | Decimal    | Variable derivada                         |
| ocean_*                    | Lógico     | One-hot de proximidad al océano           |

## Medidas DAX

```dax
-- Precio mediano global
Precio Mediano = MEDIAN(housing_clean[median_house_value])

-- Ingreso mediano global (valor real en USD)
Ingreso Mediano Real = MEDIAN(housing_clean[median_income]) * 10000

-- Total de bloques censales
Total Bloques = COUNTROWS(housing_clean)

-- Precio medio
Precio Medio = AVERAGE(housing_clean[median_house_value])
```

## Visualizaciones del dashboard (5 paneles)

### 1. Mapa de burbujas geoespacial
- **Tipo:** Mapa de burbujas (visual *ArcGIS Maps* o *Mapa* nativo)
- **Latitud:** `latitude`
- **Longitud:** `longitude`
- **Tamaño de burbuja:** `median_house_value`
- **Color:** categoría de ocean_proximity (reconstruida o columnas one-hot)
- **Descripción emergente (tooltip):** `households`, `median_income`, `median_house_value`
- **Insight:** Los bloques más caros se concentran en la bahía de San Francisco, Los Ángeles y la costa central.

### 2. Gráfico de barras – Precio por proximidad al océano
- **Tipo:** Gráfico de barras agrupadas
- **Eje X:** `ocean_proximity` (5 categorías)
- **Eje Y:** `Precio Mediano` (medida DAX)
- **Ordenar:** descendente por precio mediano
- **Formato eje Y:** moneda USD sin decimales
- **Insight:** ISLAND tiene el precio más alto (mediana ~380.000 USD); INLAND el más bajo (~120.000 USD).

### 3. Scatter – Ingreso vs Precio
- **Tipo:** Gráfico de dispersión
- **Eje X:** `median_income` (ingreso mediano del bloque)
- **Eje Y:** `median_house_value` (precio mediano)
- **Tamaño de punto:** `population`
- **Color:** ninguno (o por categoría de ocean_proximity)
- **Línea de tendencia:** activar en el panel *Análisis* de Power BI
- **Insight:** Correlación positiva clara (r = 0,688). A mayor ingreso del bloque, mayor precio mediano de la vivienda.

### 4. Tarjetas KPI
Insertar cuatro tarjetas (`Card`) con las medidas:
- **Precio Mediano** → formato: `$#,##0`
- **Ingreso Mediano Real** → formato: `$#,##0`
- **Total Bloques** → formato: número entero
- **Precio Medio** → formato: `$#,##0`

### 5. Histograma de precios
- **Tipo:** Histograma (requiere el visual *Histogram Chart* de la galería de Power BI, o usar un gráfico de columnas agrupadas sobre bins calculados)
- **Eje X:** rangos de precio (0-100K, 100K-200K, …, 400K-500K, >500K)
- **Eje Y:** recuento de bloques
- **Color de resalte:** barra ">500K" en rojo para destacar el techo artificial de 500.001 USD

## Segmentaciones (slicers)

| Slicer                  | Tipo       | Campo                    |
|-------------------------|------------|--------------------------|
| Proximidad al océano    | Lista       | `ocean_proximity`        |
| Rango de precio         | Deslizador  | `median_house_value`     |
| Rango de ingresos       | Deslizador  | `median_income`          |
| Edad de las viviendas   | Deslizador  | `housing_median_age`     |

## Diseño y tematización

- **Tema:** Power BI predeterminado o tema personalizado en azul/gris corporativo.
- **Fondo:** blanco con separadores grises suaves.
- **Tipografía:** Segoe UI, tamaño 11 para etiquetas, 14 para títulos de visual.
- **Disposición sugerida:**
  ```
  ┌─────────────────────────────────────────────────────┐
  │  [KPI Precio Mediano] [KPI Ingreso] [KPI Bloques]  │
  ├─────────────────────┬───────────────────────────────┤
  │  Mapa geoespacial   │  Barras por ocean_proximity   │
  │  (grande)           │  Scatter ingreso vs precio    │
  ├─────────────────────┴───────────────────────────────┤
  │  Histograma de precios  │  Slicers                  │
  └─────────────────────────────────────────────────────┘
  ```

## Publicación

1. Guardar como `powerbi/california_housing.pbix`.
2. En Power BI Service: **Publicar → Mi área de trabajo**.
3. Compartir el enlace del informe publicado con los miembros del equipo.
