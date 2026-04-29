-- ============================================================
-- CONSULTAS BigQuery – Proyecto Big Data: California Housing
-- Tabla: proyecto_bigdata.housing
-- Cada registro = un bloque censal de California (20.640 total)
-- ============================================================


-- ------------------------------------------------------------
-- 1. RECUENTO TOTAL DE REGISTROS
-- ------------------------------------------------------------
SELECT COUNT(*) AS total_bloques_censales
FROM `proyecto_bigdata.housing`;
-- Resultado esperado: 20.640


-- ------------------------------------------------------------
-- 2. ESTADÍSTICAS DESCRIPTIVAS DE LAS VARIABLES NUMÉRICAS
--    (media, mínimo, máximo, desviación estándar)
-- ------------------------------------------------------------
SELECT
    -- Precio mediano de vivienda (USD)
    ROUND(AVG(median_house_value), 2)    AS precio_medio,
    ROUND(MIN(median_house_value), 2)    AS precio_min,
    ROUND(MAX(median_house_value), 2)    AS precio_max,
    ROUND(STDDEV(median_house_value), 2) AS precio_desv,

    -- Ingreso mediano del bloque (decenas de miles USD)
    ROUND(AVG(median_income), 4)         AS ingreso_medio,
    ROUND(MIN(median_income), 4)         AS ingreso_min,
    ROUND(MAX(median_income), 4)         AS ingreso_max,

    -- Edad mediana de las viviendas (años)
    ROUND(AVG(housing_median_age), 2)    AS edad_media,
    ROUND(MIN(housing_median_age), 2)    AS edad_min,
    ROUND(MAX(housing_median_age), 2)    AS edad_max,

    -- Variables de tamaño del bloque
    ROUND(AVG(total_rooms), 2)           AS habitaciones_totales_media,
    ROUND(AVG(total_bedrooms), 2)        AS dormitorios_totales_media,
    ROUND(AVG(population), 2)            AS poblacion_media,
    ROUND(AVG(households), 2)            AS hogares_media
FROM `proyecto_bigdata.housing`;


-- ------------------------------------------------------------
-- 3. PRECIO MEDIANO POR CATEGORÍA DE PROXIMIDAD AL OCÉANO
--    (ordenado de mayor a menor precio)
-- ------------------------------------------------------------
SELECT
    ocean_proximity                          AS proximidad_oceano,
    COUNT(*)                                 AS num_bloques,
    ROUND(AVG(median_house_value), 0)        AS precio_medio_usd,
    ROUND(MIN(median_house_value), 0)        AS precio_min_usd,
    ROUND(MAX(median_house_value), 0)        AS precio_max_usd,
    -- Mediana aproximada con PERCENTILE_CONT
    ROUND(PERCENTILE_CONT(median_house_value, 0.5)
          OVER (PARTITION BY ocean_proximity), 0) AS precio_mediana_usd
FROM `proyecto_bigdata.housing`
GROUP BY ocean_proximity
ORDER BY precio_medio_usd DESC;
-- Categorías: <1H OCEAN, INLAND, NEAR OCEAN, NEAR BAY, ISLAND


-- ------------------------------------------------------------
-- 4. DETECCIÓN DE NULOS POR COLUMNA
--    (solo total_bedrooms debería tener 207 nulos en el CSV original)
-- ------------------------------------------------------------
SELECT
    COUNTIF(longitude IS NULL)          AS nulos_longitude,
    COUNTIF(latitude IS NULL)           AS nulos_latitude,
    COUNTIF(housing_median_age IS NULL) AS nulos_edad,
    COUNTIF(total_rooms IS NULL)        AS nulos_habitaciones,
    COUNTIF(total_bedrooms IS NULL)     AS nulos_dormitorios,
    COUNTIF(population IS NULL)         AS nulos_poblacion,
    COUNTIF(households IS NULL)         AS nulos_hogares,
    COUNTIF(median_income IS NULL)      AS nulos_ingreso,
    COUNTIF(median_house_value IS NULL) AS nulos_precio,
    COUNTIF(ocean_proximity IS NULL)    AS nulos_oceano
FROM `proyecto_bigdata.housing`;


-- ------------------------------------------------------------
-- 5. TOP 10 BLOQUES CENSALES CON MAYOR PRECIO MEDIANO
-- ------------------------------------------------------------
SELECT
    longitude,
    latitude,
    ocean_proximity,
    housing_median_age,
    households,
    median_income,
    median_house_value
FROM `proyecto_bigdata.housing`
ORDER BY median_house_value DESC
LIMIT 10;
-- Nota: el precio máximo es 500.001 USD (techo artificial del dataset)


-- ------------------------------------------------------------
-- 6. DISTRIBUCIÓN DE LA EDAD MEDIANA DE LAS VIVIENDAS
--    agrupada en rangos de 10 años
-- ------------------------------------------------------------
SELECT
    CASE
        WHEN housing_median_age BETWEEN  1 AND 10 THEN ' 1-10 años'
        WHEN housing_median_age BETWEEN 11 AND 20 THEN '11-20 años'
        WHEN housing_median_age BETWEEN 21 AND 30 THEN '21-30 años'
        WHEN housing_median_age BETWEEN 31 AND 40 THEN '31-40 años'
        WHEN housing_median_age BETWEEN 41 AND 52 THEN '41-52 años'
        ELSE 'Otro'
    END AS rango_edad,
    COUNT(*)                              AS num_bloques,
    ROUND(AVG(median_house_value), 0)     AS precio_medio_usd
FROM `proyecto_bigdata.housing`
GROUP BY rango_edad
ORDER BY rango_edad;


-- ------------------------------------------------------------
-- 7. BLOQUES CENSALES CON INGRESOS ALTOS (> 10 → > 100.000 USD reales)
--    (median_income está en decenas de miles: 10 = 100.000 USD)
-- ------------------------------------------------------------
SELECT
    longitude,
    latitude,
    ocean_proximity,
    ROUND(median_income * 10000, 0)    AS ingreso_real_usd,
    median_house_value
FROM `proyecto_bigdata.housing`
WHERE median_income > 10
ORDER BY median_income DESC;
-- Interpretación: cada unidad de median_income equivale a 10.000 USD reales
