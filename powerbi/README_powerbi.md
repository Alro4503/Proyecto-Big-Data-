# Power BI – Dashboard California Housing

El archivo `california_housing.pbix` contiene el dashboard interactivo construido sobre `data/housing.csv`.

## Visualizaciones

- **Mapa de burbujas** — distribución geográfica del precio por bloque censal. El tamaño de cada burbuja representa el precio mediano y el color la categoría de proximidad al océano. Los clústeres de precio alto coinciden con el Área de la Bahía de San Francisco y Los Ángeles.
- **Gráfico de barras** — precio mediano por categoría de `ocean_proximity`, ordenado de mayor a menor. ISLAND y NEAR BAY superan los 250.000 USD; INLAND no llega a 120.000 USD.
- **Scatter** — ingreso mediano vs precio de vivienda. Muestra la correlación positiva (r = 0,688): a mayor ingreso del bloque, mayor precio.
- **Tarjetas KPI** — precio mediano, precio medio, ingreso mediano real e total de bloques censales.

## Medidas DAX

```dax
Precio Mediano     = MEDIAN(housing[median_house_value])
Precio Medio       = AVERAGE(housing[median_house_value])
Ingreso Mediano USD = MEDIAN(housing[median_income]) * 10000
Total Bloques      = COUNTROWS(housing)
```

## Filtros

Tres slicers interactivos: proximidad al océano (lista), rango de precio y rango de ingresos (deslizadores). Al aplicar cualquier filtro se actualizan todos los visuales simultáneamente.
