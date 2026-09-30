import streamlit as st

# 1. Configuración de la página web
st.set_page_config(
    page_title="Salud Pública Caquetá", 
    page_icon="🏥", 
    layout="wide"
)

# Estilo personalizado para la identidad institucional
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

# 3. Menú de navegación lateral (Añadida la opción de Boletines)
st.sidebar.image("https://flaticon.com", width=100)
st.sidebar.title("Módulos de Salud")
st.sidebar.write("Filtre y visualice los reportes disponibles:")

opcion = st.sidebar.radio(
    "Seleccione un Tablero o Módulo:",
    [
        "📌 Vigilancia Epidemiológica", 
        "📊 Estadísticas Vitales",
        "📄 Boletines Epidemiológicos"
    ]
)

# 4. Diccionario de URLs de Power BI
urls_powerbi = {
    "📌 Vigilancia Epidemiológica": "https://powerbi.com",
    "📊 Estadísticas Vitales": "https://powerbi.com"
}

# 5. Lógica de renderizado según la selección del usuario
if opcion == "📄 Boletines Epidemiológicos":
    st.subheader("📄 Histórico de Boletines Epidemiológicos")
    st.write("Consulte y descargue los documentos oficiales emitidos por el equipo de vigilancia epidemiológica departamental:")
    
    # Diseño en cuadrícula para organizar los archivos ordenadamente
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("📅 Boletines Año 2026")
        # Copia la estructura del botón reemplazando las URL por los enlaces de tus archivos PDF
        st.link_button("📥 Descargar Boletín Epidemiológico - Semana 03", "https://enlace_a_tu_pdf_en_google_drive.com")
        st.link_button("📥 Descargar Boletín Epidemiológico - Semana 02", "https://enlace_a_tu_pdf_en_google_drive.com")
        st.link_button("📥 Descargar Boletín Epidemiológico - Semana 01", "https://enlace_a_tu_pdf_en_google_drive.com")

    with col2:
        st.dark_note = "📅 Históricos Anteriores"
        st.write("Para revisar períodos epidemiológicos de años previos, comuníquese con el área de sistemas o consulte el archivo físico institucional.")

else:
    # Si elige un tablero de control, se renderiza el iframe interactivo normal
    st.subheader(f"Visualizando: {opcion}")
    url_activa = urls_powerbi[opcion]
    st.components.v1.iframe(url_activa, height=700, scrolling=True)

# Pie de página institucional
st.markdown("---")
st.caption("© 2026 Área de Salud Pública - Departamento del Caquetá. Información para uso estrictamente informativo y estadístico.")