import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from st_aggrid import AgGrid
import datetime
from io import BytesIO

# Configuración inicial de la página
st.set_page_config(
    page_title="Modern Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main {
        background-color: #F5F5F5;
    }
    .header {
        color: #1E3A8A;
        font-size: 40px;
        padding: 20px;
    }
    .metric-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .sidebar .sidebar-content {
        background-color: #1E3A8A;
    }
</style>
""", unsafe_allow_html=True)

# Generar datos de ejemplo
@st.cache_data
def generate_sample_data():
    date_range = pd.date_range(start='2023-01-01', end='2023-12-31')
    categories = ['Electronics', 'Fashion', 'Home', 'Beauty', 'Sports']
    data = pd.DataFrame({
        'Date': np.random.choice(date_range, 500),
        'Category': np.random.choice(categories, 500),
        'Sales': np.random.randint(100, 5000, 500),
        'Profit': np.random.uniform(10, 2000, 500)
    })
    return data

# Cargar datos
def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            return pd.read_csv(uploaded_file)
        except:
            return pd.read_excel(uploaded_file)
    return generate_sample_data()

# Sidebar
with st.sidebar:
    st.title("⚙️ Configuración")
    uploaded_file = st.file_uploader("Subir archivo (CSV/Excel)", type=['csv', 'xlsx'])
    st.divider()
    
    # Filtros
    st.header("Filtros")
    min_date = st.date_input("Fecha inicial", datetime.date(2023, 1, 1))
    max_date = st.date_input("Fecha final", datetime.date(2023, 12, 31))

# Cargar datos
df = load_data(uploaded_file)
df['Date'] = pd.to_datetime(df['Date'])

# Aplicar filtros
mask = (df['Date'].dt.date >= min_date) & (df['Date'].dt.date <= max_date)
filtered_df = df[mask]

# Header
st.markdown('<h1 class="header">📈 Modern Analytics Dashboard</h1>', unsafe_allow_html=True)

# Métricas clave
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-card">💰 Ventas Totales<br><h2>${:,.0f}</h2></div>'.format(filtered_df['Sales'].sum()), unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card">📈 Beneficio Promedio<br><h2>${:,.2f}</h2></div>'.format(filtered_df['Profit'].mean()), unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card">🏷️ Categorías Únicas<br><h2>{}</h2></div>'.format(filtered_df['Category'].nunique()), unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-card">📅 Rango Fechas<br><h2>{} - {}</h2></div>'.format(min_date.strftime("%d/%m/%y"), max_date.strftime("%d/%m/%y")), unsafe_allow_html=True)

# Gráficos
st.divider()
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Ventas por Categoría")
    fig = px.bar(filtered_df, x='Category', y='Sales', color='Category',
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)

with col_chart2:
    st.subheader("Distribución de Beneficios")
    fig = px.pie(filtered_df, names='Category', values='Profit',
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)

# Tabla interactiva
st.divider()
st.subheader("📊 Datos Detallados")
AgGrid(filtered_df, height=400, theme='streamlit', fit_columns_on_grid_load=True)

# Exportación de datos
st.divider()
col_exp1, col_exp2, col_exp3 = st.columns(3)

with col_exp1:
    buffer = BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        filtered_df.to_excel(writer, index=False)
    st.download_button("📤 Exportar a Excel", data=buffer.getvalue(), 
                      file_name="datos_exportados.xlsx",
                      mime="application/vnd.ms-excel")

with col_exp2:
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("📤 Exportar a CSV", data=csv, 
                      file_name="datos_exportados.csv",
                      mime="text/csv")

with col_exp3:
    st.button("🔄 Actualizar Datos", help="Actualizar todos los datos y visualizaciones")

# Nota para el PDF
st.markdown("""
*Para exportar a PDF: Usar la función de impresión del navegador (Ctrl+P) y seleccionar 'Guardar como PDF'*
""")
