import streamlit as st

# 1. Configuración de la página web
st.set_page_config(
    page_title="Salud Pública Caquetá",
    page_icon="logo.png",
    layout="wide"
)

# Datos editables del pie de página (si dejas uno vacío, no se muestra)
FUENTES = "Sivigila, RUAF-ND"
ACTUALIZACION = ""   # Ejemplo: "30/09/2026"
CONTACTO = ""        # Ejemplo: "vigilancia@ejemplo.gov.co"

# Estilo personalizado para la identidad institucional
st.markdown("""
    <style>
    .block-container {
        padding-top: 3rem;
    }
    [data-testid="stSidebarHeader"] {
        height: 1rem;
        padding: 0;
    }
    [data-testid="stSidebarUserContent"] {
        padding-top: 0rem;
    }
    .main-title {
        color: #0B3C8C !important;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: 700;
        font-size: 2rem !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    .sub-title {
        color: #5B6B82;
        font-size: 1.05rem;
        margin: -0.4rem 0 1rem 0 !important;
    }
    iframe {
        border: 1px solid #D9E2EF;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(11, 60, 140, 0.10);
    }
    </style>
""", unsafe_allow_html=True)

# 2. Encabezado principal de la página
st.markdown('<h1 class="main-title">Portal de Vigilancia Epidemiológica</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Salud Pública - Departamento del Caquetá</p>', unsafe_allow_html=True)
st.write("Consulte eventos de interés en salud pública, estadísticas de nacimientos y defunciones, boletines epidemiológicos oficiales y calendario epidemiológico. Seleccione un módulo en el menú de la izquierda.")

# 3. Menú de navegación lateral con logo
url_logo_estable = "logo.png"

try:
    st.sidebar.image(url_logo_estable, use_container_width=True)
except Exception:
    st.sidebar.markdown("<h3 style='text-align: center;'>🕵️‍♂️</h3>", unsafe_allow_html=True)

st.sidebar.markdown("<hr style='margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)
st.sidebar.markdown("<h2 style='text-align: center; margin-top: 0px;'>Módulos</h2>", unsafe_allow_html=True)

opcion = st.sidebar.radio(
    "Seleccione un tablero o módulo:",
    [
        "Vigilancia Epidemiológica",
        "Estadísticas Vitales",
        "Boletines Epidemiológicos",
        "Calendario Epidemiológico 2026",
        "Manual de Codificación de EISP",
    ]
)

# 4. Diccionarios de Power BI (las claves deben ser iguales a las opciones del menú)
urls_powerbi = {
    "Vigilancia Epidemiológica": "https://app.powerbi.com/view?r=eyJrIjoiYzFiOTAwMzQtN2VkNy00NDhiLThjMTItZGY3NzNhMjExMTkwIiwidCI6IjkxOTM0N2Q1LTkyMWUtNDczOC05MGJkLTJkMTU4YzUzM2QzOCIsImMiOjR9",
    "Estadísticas Vitales": "https://app.powerbi.com/view?r=eyJrIjoiNTZiZjhlMzQtOTgxNS00MDUwLTlkMjMtMDQ2OWI3ZjA5YjU0IiwidCI6IjkxOTM0N2Q1LTkyMWUtNDczOC05MGJkLTJkMTU4YzUzM2QzOCIsImMiOjR9"
}
titulos_powerbi = {
    "Vigilancia Epidemiológica": "Análisis de los Eventos de Interés en Salud Pública",
    "Estadísticas Vitales": "Cifras de Nacimientos y Defunciones del Departamento"
}
alturas_powerbi = {
    "Vigilancia Epidemiológica": 900,
    "Estadísticas Vitales": 1670
}

# 5. Lógica de renderizado según la selección del usuario
if opcion == "Boletines Epidemiológicos":
    st.subheader("Histórico de Boletines Epidemiológicos")

    with st.container(border=True):
        st.caption("Organizados por Semanas Epidemiológicas (SE).")
        st.link_button(
            "📂 Acceder a los Boletines Epidemiológicos en Google Drive",
            "https://drive.google.com/drive/folders/1tUQdlVhytJqKxA6-tBK4Yw7pThfy-X0h?usp=sharing",
            use_container_width=True,
            type="primary"
        )

    st.info(
        "💡 **Información:** Al hacer clic en el botón superior, se abrirá una pestaña segura "
        "con el listado completo de carpetas. No requiere contraseñas institucionales y puede visualizar o descargar los archivos "
        "PDF desde cualquier dispositivo."
    )

elif opcion == "Calendario Epidemiológico 2026":
    st.subheader("Calendario Epidemiológico 2026")
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image("Calendario2026.png", use_container_width=True)
        with open("Calendario2026.pdf", "rb") as f:
            st.download_button(
                "⬇️ Descargar en PDF",
                f,
                file_name="calendario_epidemiologico_2026.pdf",
                mime="application/pdf",
                use_container_width=True
            )
elif opcion == "Manual de Codificación de EISP":
    st.subheader("Manual de Codificación de EISP")
else:
    st.subheader(titulos_powerbi[opcion])
    url_activa = urls_powerbi[opcion]
    st.components.v1.iframe(url_activa, height=alturas_powerbi[opcion], scrolling=False)

# Pie de página institucional
st.markdown("---")
partes = [f"Fuentes: {FUENTES}"]
if ACTUALIZACION:
    partes.append(f"Última actualización: {ACTUALIZACION}")
if CONTACTO:
    partes.append(f"Contacto: {CONTACTO}")
st.caption("  |  ".join(partes) + "  \n© 2026 Área de Vigilancia Epidemiológica - Departamento del Caquetá. Información para uso estrictamente informativo y estadístico.")