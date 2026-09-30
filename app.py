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
st.markdown('<h1 class="main-title">Portal - Vigilancia Epidemiológica en Salud Pública - Caquetá</h1>', unsafe_allow_html=True)
st.write("Bienvenido al Sistema de Análisis Epidemiológico y Demográfico del Departamento. Aquí podrá consultar eventos de interés en salud pública, estadísticas de nacimientos y defunciones, y los boletines epidemiológicos oficiales. Seleccione un módulo en el menú de la izquierda.")

# 3. Menú de navegación lateral (Añadida la opción de Boletines)
st.sidebar.image("https://drive.google.com/uc?id=1t7nMTqXJ_yxgrUnl5xwuF-rH_EgAzbp4", width=100)
st.sidebar.title("Módulos")
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
    "📌 Vigilancia Epidemiológica": "https://app.powerbi.com/view?r=eyJrIjoiYzFiOTAwMzQtN2VkNy00NDhiLThjMTItZGY3NzNhMjExMTkwIiwidCI6IjkxOTM0N2Q1LTkyMWUtNDczOC05MGJkLTJkMTU4YzUzM2QzOCIsImMiOjR9",
    "📊 Estadísticas Vitales": "https://app.powerbi.com/view?r=eyJrIjoiNTZiZjhlMzQtOTgxNS00MDUwLTlkMjMtMDQ2OWI3ZjA5YjU0IiwidCI6IjkxOTM0N2Q1LTkyMWUtNDczOC05MGJkLTJkMTU4YzUzM2QzOCIsImMiOjR9"
}

# 5. Lógica de renderizado según la selección del usuario
if opcion == "📄 Boletines Epidemiológicos":
    st.subheader("📄 Histórico de Boletines Epidemiológicos")
    st.write("Bienvenido al repositorio oficial de documentación del Área de Vigilancia Epidemiológica.")
    
    # Caja interactiva con diseño limpio institucional
    with st.container(border=True):
        st.markdown("### 🏛️ Repositorio Digital Departamental")
        st.write(
            "Para garantizar el acceso oportuno a la información y dar cumplimiento a las normativas de "
            "salud pública, los boletines se encuentran alojados en nuestro servidor institucional en la nube."
        )
        st.write("**Organización:** Por Semanas Epidemiológicas (SE).")
        
        # EL BOTÓN PRINCIPAL CON TU ENLACE PÚBLICO CORREGIDO
        st.link_button(
            "📂 Acceder a los Boletines Epidemiológicos en Google Drive", 
            "https://drive.google.com/drive/folders/1tUQdlVhytJqKxA6-tBK4Yw7pThfy-X0h?usp=sharing",
            use_container_width=True,
            type="primary"
        )
    
    # Mensaje de orientación al ciudadano
    st.info(
        "💡 **Información para el usuario:** Al hacer clic en el botón superior, se abrirá una pestaña segura "
        "con el listado completo de carpetas. No requiere contraseñas institucionales y puede visualizar o descargar los archivos "
        "PDF de manera inmediata desde cualquier computadora o dispositivo móvil."
    )

else:
    # Si elige un tablero de control, se renderiza el iframe interactivo normal
    st.subheader(f"Visualizando: {opcion}")
    url_activa = urls_powerbi[opcion]
    st.components.v1.iframe(url_activa, height=700, scrolling=True)

# Pie de página institucional
st.markdown("---")
st.caption("© 2026 Área de Salud Pública - Departamento del Caquetá. Información para uso estrictamente informativo y estadístico.")