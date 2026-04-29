import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from scipy import stats

# ---------------------------------------------------------------------------
# Rutas: funcionan tanto en local como dentro del contenedor Docker
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.environ.get('DATA_DIR', os.path.join(BASE_DIR, 'data'))
GRAFICOS_DIR = os.environ.get('GRAFICOS_DIR', os.path.join(BASE_DIR, 'graficos'))
os.makedirs(GRAFICOS_DIR, exist_ok=True)

CSV_ENTRADA = os.path.join(DATA_DIR, 'housing.csv')
CSV_SALIDA = os.path.join(DATA_DIR, 'housing_clean.csv')

# ---------------------------------------------------------------------------
# Estilo de gráficos
# ---------------------------------------------------------------------------
try:
    plt.style.use('seaborn-v0_8-whitegrid')
except OSError:
    plt.style.use('seaborn-whitegrid')

PALETA = 'Set2'

# ---------------------------------------------------------------------------
# Formateadores en formato europeo (coma como separador decimal)
# ---------------------------------------------------------------------------
def fmt_europeo(x, pos=None):
    """Formatea número con coma decimal y punto de miles al estilo europeo."""
    if x >= 1_000_000:
        return f'{x/1_000_000:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.') + 'M'
    if x >= 1_000:
        return f'{x/1_000:,.1f}'.replace(',', 'X').replace('.', ',').replace('X', '.') + 'K'
    return f'{x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

def fmt_precio(x, pos=None):
    return f'{x/1_000:.0f}K'

def fmt_miles(x, pos=None):
    return f'{int(x):,}'.replace(',', '.')


# ===========================================================================
# [1] CARGA Y EXPLORACIÓN INICIAL
# ===========================================================================
print('=' * 60)
print('[1] CARGA Y EXPLORACIÓN INICIAL')
print('=' * 60)

if not os.path.exists(CSV_ENTRADA):
    print(f'ERROR: No se encontró {CSV_ENTRADA}')
    print('Coloca housing.csv en la carpeta data/ y vuelve a ejecutar.')
    sys.exit(1)

df = pd.read_csv(CSV_ENTRADA)

print(f'\nDimensiones del dataset: {df.shape[0]:,} filas × {df.shape[1]} columnas')
print('\nPrimeras 5 filas:')
print(df.head().to_string())
print('\nTipos de datos:')
print(df.dtypes.to_string())
print('\nValores nulos por columna:')
print(df.isnull().sum().to_string())


# ===========================================================================
# [2] ESTADÍSTICAS DESCRIPTIVAS
# ===========================================================================
print('\n' + '=' * 60)
print('[2] ESTADÍSTICAS DESCRIPTIVAS')
print('=' * 60)

desc = df.describe().T
desc.index.name = 'variable'
print(desc.to_string())

print('\nDistribución de ocean_proximity:')
print(df['ocean_proximity'].value_counts().to_string())


# ===========================================================================
# [3] LIMPIEZA Y TRANSFORMACIÓN
# ===========================================================================
print('\n' + '=' * 60)
print('[3] LIMPIEZA Y TRANSFORMACIÓN')
print('=' * 60)

# Imputar nulos de total_bedrooms con la mediana
nulos_antes = df['total_bedrooms'].isnull().sum()
mediana_tb = df['total_bedrooms'].median()
df['total_bedrooms'] = df['total_bedrooms'].fillna(mediana_tb)
print(f'Nulos en total_bedrooms imputados con mediana ({mediana_tb:.1f}): {nulos_antes} registros')

# Variables derivadas a nivel de bloque censal
df['rooms_per_household'] = df['total_rooms'] / df['households']
df['bedrooms_per_room'] = df['total_bedrooms'] / df['total_rooms']
df['population_per_household'] = df['population'] / df['households']
print('Variables derivadas creadas: rooms_per_household, bedrooms_per_room, population_per_household')

# Eliminar bloques con valores claramente atípicos en population_per_household
antes = len(df)
df = df[df['population_per_household'] < 20]
print(f'Filas eliminadas por population_per_household >= 20: {antes - len(df)}')

# One-hot encoding para ocean_proximity
df = pd.get_dummies(df, columns=['ocean_proximity'], prefix='ocean', drop_first=False)
print(f'One-hot encoding aplicado. Nuevas dimensiones: {df.shape}')
print(f'\nDataset limpio: {len(df):,} bloques censales')


# ===========================================================================
# [4] GRÁFICO 1 – Histograma de median_house_value
# ===========================================================================
print('\n' + '=' * 60)
print('[4] GRÁFICO 1 – Histograma de precios')
print('=' * 60)

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(df['median_house_value'], bins=50, color='steelblue', edgecolor='white', linewidth=0.5)

ax.xaxis.set_major_formatter(ticker.FuncFormatter(fmt_precio))
ax.yaxis.set_major_formatter(ticker.FuncFormatter(fmt_miles))

ax.axvline(500_001, color='crimson', linestyle='--', linewidth=1.5,
           label='Techo artificial: 500.001 USD')
ax.axvline(df['median_house_value'].median(), color='darkorange', linestyle='-', linewidth=1.5,
           label=f'Mediana: {df["median_house_value"].median()/1000:.0f}K USD')

ax.set_title('Distribución del Precio Mediano de Vivienda\npor Bloque Censal – California', fontsize=14, pad=12)
ax.set_xlabel('Precio mediano (USD)', fontsize=12)
ax.set_ylabel('Número de bloques censales', fontsize=12)
ax.legend(fontsize=10)
ax.tick_params(axis='both', labelsize=9)

plt.tight_layout()
ruta = os.path.join(GRAFICOS_DIR, '01_histograma_precios.png')
plt.savefig(ruta, dpi=150, bbox_inches='tight')
plt.close()
print(f'Guardado: {ruta}')


# ===========================================================================
# [5] GRÁFICO 2 – Scatter: median_income vs median_house_value
# ===========================================================================
print('\n' + '=' * 60)
print('[5] GRÁFICO 2 – Scatter ingresos vs precio')
print('=' * 60)

slope, intercept, r_value, p_value, std_err = stats.linregress(
    df['median_income'], df['median_house_value']
)
print(f'Regresión lineal: r = {r_value:.3f}, p = {p_value:.2e}')

muestra = df.sample(n=min(3000, len(df)), random_state=42)

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(muestra['median_income'], muestra['median_house_value'],
           alpha=0.3, s=10, color='steelblue', label='Bloques censales (muestra)')

x_line = np.linspace(df['median_income'].min(), df['median_income'].max(), 200)
ax.plot(x_line, slope * x_line + intercept, color='crimson', linewidth=2,
        label=f'Regresión lineal  r = {r_value:.3f}')

ax.yaxis.set_major_formatter(ticker.FuncFormatter(fmt_precio))
ax.set_title('Ingreso Mediano vs Precio Mediano de Vivienda\n(r = 0,688 — mayor correlación del dataset)',
             fontsize=13, pad=12)
ax.set_xlabel('Ingreso mediano del bloque (decenas de miles USD)', fontsize=12)
ax.set_ylabel('Precio mediano de vivienda (USD)', fontsize=12)
ax.legend(fontsize=10)
ax.tick_params(axis='both', labelsize=9)

plt.tight_layout()
ruta = os.path.join(GRAFICOS_DIR, '02_scatter_ingresos_precio.png')
plt.savefig(ruta, dpi=150, bbox_inches='tight')
plt.close()
print(f'Guardado: {ruta}')


# ===========================================================================
# [6] GRÁFICO 3 – Boxplots por ocean_proximity
# ===========================================================================
print('\n' + '=' * 60)
print('[6] GRÁFICO 3 – Boxplots por proximidad al océano')
print('=' * 60)

# Reconstruir columna ocean_proximity desde one-hot para el gráfico
ocean_cols = [c for c in df.columns if c.startswith('ocean_')]
df_box = df.copy()
df_box['ocean_proximity'] = df_box[ocean_cols].idxmax(axis=1).str.replace('ocean_', '', regex=False)

orden = (df_box.groupby('ocean_proximity')['median_house_value']
         .median().sort_values(ascending=False).index.tolist())

fig, ax = plt.subplots(figsize=(11, 6))
sns.boxplot(data=df_box, x='ocean_proximity', y='median_house_value',
            order=orden, palette=PALETA, ax=ax, fliersize=2)

ax.yaxis.set_major_formatter(ticker.FuncFormatter(fmt_precio))
ax.set_title('Precio Mediano de Vivienda según Proximidad al Océano\n(bloques censales de California)',
             fontsize=13, pad=12)
ax.set_xlabel('Proximidad al océano', fontsize=12)
ax.set_ylabel('Precio mediano (USD)', fontsize=12)
ax.tick_params(axis='both', labelsize=9)

plt.tight_layout()
ruta = os.path.join(GRAFICOS_DIR, '03_boxplot_ocean_proximity.png')
plt.savefig(ruta, dpi=150, bbox_inches='tight')
plt.close()
print(f'Guardado: {ruta}')

medianas = df_box.groupby('ocean_proximity')['median_house_value'].median().sort_values(ascending=False)
for cat, val in medianas.items():
    print(f'  {cat:15s}: {val:,.0f} USD')


# ===========================================================================
# [7] GRÁFICO 4 – Heatmap de correlaciones
# ===========================================================================
print('\n' + '=' * 60)
print('[7] GRÁFICO 4 – Heatmap de correlaciones')
print('=' * 60)

cols_corr = [
    'median_house_value', 'median_income', 'housing_median_age',
    'total_rooms', 'total_bedrooms', 'population', 'households',
    'rooms_per_household', 'bedrooms_per_room', 'population_per_household'
]
corr_matrix = df[cols_corr].corr()

fig, ax = plt.subplots(figsize=(11, 9))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdYlGn',
            center=0, vmin=-1, vmax=1, linewidths=0.5,
            annot_kws={'size': 8}, ax=ax)
ax.set_title('Mapa de Correlaciones – Dataset California Housing\n(triángulo inferior)', fontsize=13, pad=12)
ax.tick_params(axis='both', labelsize=9)
plt.xticks(rotation=30, ha='right')
plt.yticks(rotation=0)

plt.tight_layout()
ruta = os.path.join(GRAFICOS_DIR, '04_heatmap_correlaciones.png')
plt.savefig(ruta, dpi=150, bbox_inches='tight')
plt.close()
print(f'Guardado: {ruta}')

corr_precio = corr_matrix['median_house_value'].drop('median_house_value').sort_values(ascending=False)
print('Correlación con median_house_value:')
for var, val in corr_precio.items():
    print(f'  {var:30s}: {val:+.3f}')


# ===========================================================================
# [8] GRÁFICO 5 – Mapa geoespacial
# ===========================================================================
print('\n' + '=' * 60)
print('[8] GRÁFICO 5 – Mapa geoespacial de California')
print('=' * 60)

fig, ax = plt.subplots(figsize=(10, 8))

sc = ax.scatter(
    df['longitude'], df['latitude'],
    c=df['median_house_value'],
    s=df['population'] / 100,
    alpha=0.4,
    cmap='plasma',
    vmin=df['median_house_value'].quantile(0.05),
    vmax=df['median_house_value'].quantile(0.95)
)
cbar = plt.colorbar(sc, ax=ax, fraction=0.03, pad=0.04)
cbar.set_label('Precio mediano (USD)', fontsize=10)
cbar.ax.yaxis.set_major_formatter(ticker.FuncFormatter(fmt_precio))

ax.set_title('Distribución Geoespacial del Precio de Vivienda – California\n'
             '(tamaño del punto ∝ población del bloque)',
             fontsize=13, pad=12)
ax.set_xlabel('Longitud', fontsize=11)
ax.set_ylabel('Latitud', fontsize=11)
ax.tick_params(axis='both', labelsize=9)
ax.set_xlim(-124.5, -114.0)
ax.set_ylim(32.5, 42.0)

plt.tight_layout()
ruta = os.path.join(GRAFICOS_DIR, '05_mapa_geoespacial.png')
plt.savefig(ruta, dpi=150, bbox_inches='tight')
plt.close()
print(f'Guardado: {ruta}')


# ===========================================================================
# [9] ESTANDARIZACIÓN Z-SCORE Y EXPORTACIÓN
# ===========================================================================
print('\n' + '=' * 60)
print('[9] ESTANDARIZACIÓN Z-SCORE Y EXPORTACIÓN')
print('=' * 60)

cols_num = [
    'longitude', 'latitude', 'housing_median_age',
    'total_rooms', 'total_bedrooms', 'population', 'households',
    'median_income', 'median_house_value',
    'rooms_per_household', 'bedrooms_per_room', 'population_per_household'
]

df_clean = df.copy()
for col in cols_num:
    if col in df_clean.columns:
        mu = df_clean[col].mean()
        sigma = df_clean[col].std()
        df_clean[f'{col}_z'] = (df_clean[col] - mu) / sigma

df_clean.to_csv(CSV_SALIDA, sep=',', decimal='.', index=False, encoding='utf-8')
print(f'Dataset limpio exportado: {CSV_SALIDA}')
print(f'Filas: {len(df_clean):,}  |  Columnas: {df_clean.shape[1]}')

print('\n' + '=' * 60)
print('ANÁLISIS COMPLETADO')
print(f'  Gráficos en: {GRAFICOS_DIR}')
print(f'  CSV limpio en: {CSV_SALIDA}')
print('=' * 60)
