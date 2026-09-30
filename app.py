import streamlit as st

# 1. Configuración de la página web
st.set_page_config(
    page_title="Salud Pública Caquetá", 
    page_icon="🏥", 
    layout="wide"
)

# Estilo personalizado para la identidad institucional (Verde/Azul institucional)
st.markdown("""
    <style>
    .main-title {
        color: #006699;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: bold;
        padding-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Encabezado principal de la página
st.markdown('<h1 class="main-title">🏥 Portal de Control - Salud Pública de Caquetá</h1>', unsafe_allow_html=True)
st.write("Bienvenido al sistema de visualización de indicadores de salud pública del departamento. Seleccione un módulo en el menú de la izquierda.")

# 3. Menú de navegación lateral
st.sidebar.image("https://flaticon.com", width=100) # Icono opcional
st.sidebar.title("Módulos de Salud")
st.sidebar.write("Filtre y visualice los reportes disponibles:")

# Opciones actualizadas (Eliminados vacunación e infantil; renombrado estadísticas)
opcion = st.sidebar.radio(
    "Seleccione un Tablero:",
    [
        "📌 Vigilancia Epidemiológica", 
        "📊 Estadísticas Vitales"
    ]
)

# 4. Diccionario de URLs de Power BI (Estructura limpia actualizada)
urls_powerbi = {
    "📌 Vigilancia Epidemiológica": "https://powerbi.com",
    "📊 Estadísticas Vitales": "https://powerbi.com"
}

# 4. Diccionario de URLs de Power BI (Reemplaza con tus enlaces "Publicar en la Web")
urls_powerbi = {
    "📌 Vigilancia Epidemiológica": "https://app.powerbi.com/view?r=eyJrIjoiYzFiOTAwMzQtN2VkNy00NDhiLThjMTItZGY3NzNhMjExMTkwIiwidCI6IjkxOTM0N2Q1LTkyMWUtNDczOC05MGJkLTJkMTU4YzUzM2QzOCIsImMiOjR9",
    "📊 Estadísticas Vitales": "https://app.powerbi.com/view?r=eyJrIjoiNTZiZjhlMzQtOTgxNS00MDUwLTlkMjMtMDQ2OWI3ZjA5YjU0IiwidCI6IjkxOTM0N2Q1LTkyMWUtNDczOC05MGJkLTJkMTU4YzUzM2QzOCIsImMiOjR9"
}

# 5. Renderizado del Tablero de Control seleccionado
st.subheader(f"Visualizando: {opcion}")

# Usamos un contenedor contenedor responsivo para el iframe de Power BI
url_activa = urls_powerbi[opcion]

# El iframe incrusta el reporte directo en la interfaz web de Python
st.components.v1.iframe(url_activa, height=700, scrolling=True)

# Pie de página institucional
st.markdown("---")
st.caption("© 2026 Área de Salud Pública - Departamento del Caquetá. Información para uso estrictamente informativo y estadístico.")
