import base64
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
    @import url('https://googleapis.com');
    
    /* ---- Tipografía ---- */
    .stApp {
        font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif !important;
    }
    h1, h2, h3, h4 {
        font-family: 'Poppins', 'Helvetica Neue', Arial, sans-serif !important;
        font-weight: 700 !important;
    }
    [data-testid="stCaptionContainer"] {
        color: #4A5568 !important;
    }
    
    /* ---- Espaciado general ---- */
    .block-container {
        padding-top: 3rem;
    }
    [data-testid="stSidebarHeader"] {
        height: 1rem;
        padding: 0;
    }
    [data-testid="stSidebarUserContent"] {
        padding-top: 1rem;
    }
    
        /* ---- Barra lateral: Fondo azul grisáceo y estructura ---- */
    [data-testid="stSidebar"],
    [data-testid="stSidebarContent"] {
        background-color: #F1F5F9 !important; /* Fondo estructurado */
    }
    [data-testid="stSidebar"] {
        border-right: 1px solid #E2E8F0;
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.3rem;
    }
    [data-testid="stSidebar"] button {
        justify-content: flex-start;
        text-align: left;
        border-radius: 8px;
        padding: 0.55rem 0.75rem;
        min-height: 0;
        transition: all 0.2s ease-in-out; /* Animación suave */
    }
    [data-testid="stSidebar"] button > div {
        justify-content: flex-start;
        width: 100%;
    }
        /* ---- Agrandar el texto y el icono del Link Button (Boletines) ---- */
    [data-testid="stLinkButton"] a p {
        font-size: 1.15rem !important; /* Aumenta el tamaño del texto */
        font-weight: 600 !important;   /* Lo hace un poco más grueso y legible */
        letter-spacing: 0.3px;         /* Da una separación elegante a las letras */
    }
    
    [data-testid="stLinkButton"] a span {
        font-size: 1.25rem !important; /* Aumenta ligeramente el tamaño del emoji de la carpeta */
    }
    /* ---- ADAPTACIÓN AUTOMÁTICA PARA CELULARES (Pantallas menores a 768px) ---- */
    @media (max-width: 768px) {
        /* 1. Hace que las tarjetas se apilen una debajo de la otra en vertical */
        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: 1.5rem !important;
        }
        
        /* 2. Permite que las tarjetas reduzcan su altura fija en celular para que no sobre espacio */
        [class*="st-key-card_"] {
            min-height: auto !important; 
            padding: 1.2rem !important;
        }
        
        /* 3. Escala los iconos de forma fluida para que se adapten a la pantalla del teléfono */
        [class*="st-key-card_"] img {
            max-width: 140px !important; /* Tamaño ligeramente menor y cómodo para pantallas móviles */
            height: auto !important;
        }

        /* 4. Ajusta el tamaño de la tipografía principal para que no ocupe toda la pantalla del celular */
        .hero-title {
            font-size: 1.9rem !important;
        }
        .hero-sub {
            font-size: 1.05rem !important;
        }
    }

    /* Botones NO seleccionados (Estado normal) */
    [data-testid="stSidebar"] button[kind="secondary"],
    [data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {
        background: #FFFFFF !important; /* Fondo blanco */
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }
    [data-testid="stSidebar"] button[kind="secondary"] p,
    [data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] p {
        color: #4A5568 !important; /* Texto gris oscuro */
        font-weight: 500;
    }
    
    /* Botones NO seleccionados (Al pasar el cursor por encima) */
    [data-testid="stSidebar"] button[kind="secondary"]:hover,
    [data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover {
        background: #0B3C8C !important; /* Se pinta de azul oscuro */
        border-color: #0B3C8C !important;
    }
    [data-testid="stSidebar"] button[kind="secondary"]:hover p,
    [data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover p {
        color: #FFFFFF !important; /* Texto cambia a blanco */
    }
    
    /* Botón SELECCIONADO (Módulo activo permanente) */
    [data-testid="stSidebar"] button[kind="primary"],
    [data-testid="stSidebar"] [data-testid="stBaseButton-primary"] {
        background: #0B3C8C !important; /* Azul oscuro sólido fijo */
        border: 1px solid #0B3C8C !important;
        box-shadow: 0 4px 6px rgba(11, 60, 140, 0.2) !important;
    }
    [data-testid="stSidebar"] button[kind="primary"] p,
    [data-testid="stSidebar"] [data-testid="stBaseButton-primary"] p {
        color: #FFFFFF !important; /* Texto blanco fijo */
        font-weight: 700;
    }
        /* ---- Agrandar el texto y espacio del botón de descarga ---- */
    [data-testid="stMain"] button[kind="secondary"] p,
    [data-testid="stMain"] [data-testid="stBaseButton-secondary"] p {
        font-size: 1.15rem !important; /* Aumenta el tamaño de la letra */
        font-weight: 600 !important;   /* Lo hace un poco más grueso y legible */
    }

    /* ---- Centrado y tamaño del título Módulos ---- */
    .nav-label {
        font-size: 1.15rem !important; /* Tamaño más grande y visible */
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        color: #000000 !important; /* Azul institucional */
        text-align: center;
        margin: 1.2rem 0 1rem 0 !important; /* Mayor separación de la línea superior */
    }
    
    /* ---- Encabezado de los módulos ---- */
    .main-title {
        color: #0B3C8C !important;
        font-size: 2rem !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    .sub-title {
        color: #4A5568;
        font-size: 1.05rem;
        margin: -0.4rem 0 1rem 0 !important;
    }
    
    /* ---- Portada (hero sin gráfica) ---- */
    .hero-title {
        color: #0B3C8C !important;
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        line-height: 1.2 !important;
        padding: 0 !important;
        margin: 0 0 0.5rem 0 !important;
    }
    .hero-sub {
        color: #1E293B;
        font-size: 1.25rem;
        font-weight: 500;
        line-height: 1.5;
        margin: 0 0 1.5rem 0;
    }
    .texto {
        color: #4A5568;
        font-size: 1.05rem;
        line-height: 1.65;
        margin: 0 0 1rem 0;
    }
    
        /* ---- Estilizado y simetría de Tarjetas Informativas (Forzar igual tamaño) ---- */
    [class*="st-key-card_"] {
        background: #FFFFFF;
        border: 1px solid #E5EAF2 !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 14px rgba(11, 60, 140, 0.05);
        padding: 1.5rem !important;
        min-height: 320px !important; /* <--- ESTA LÍNEA OBLIGA A QUE TODAS MIDAN LO MISMO */
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
    }


        /* ---- Estilo del Título de la Tarjeta ---- */
    .card-titulo {
        font-family: 'Poppins', 'Helvetica Neue', Arial, sans-serif;
        font-size: 1.15rem !important; /* Reducido levemente de 1.25rem para mejor equilibrio */
        font-weight: 700;
        color: #0B3C8C;
        margin: 0.5rem 0 0.3rem 0 !important; /* Espaciado compacto */
    }

    /* ---- Estilo del Párrafo descriptivo ---- */
    .card-descripcion {
        color: #4A5568;
        font-size: 0.88rem !important; /* Estilizado de 0.95rem a 0.88rem (Más limpio) */
        line-height: 1.45;
    }

    
    /* ---- Tableros ---- */
    iframe {
        border: 1px solid #D9E2EF;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(11, 60, 140, 0.10);
    }
    </style>
""", unsafe_allow_html=True)

def svg_a_img(svg, ancho="100%"):
    """Incrusta un SVG como imagen para que Markdown no lo altere."""
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f'<img src="data:image/svg+xml;base64,{b64}" style="width:{ancho};" />'

def icono(trazos):
    """Ícono de línea en azul institucional (24x24) con URL XML corregida."""
    return (
        '<svg xmlns="http://w3.org" viewBox="0 0 24 24" fill="none" '
        'stroke="#0B3C8C" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
        + trazos + '</svg>'
    )

ICONO_TABLERO = (
    '<div style="text-align: center; margin-bottom: 0.5rem;">'
    '<svg xmlns="http://w3.org" width="48" height="48" viewBox="0 0 24 24" fill="none" '
    'stroke="#0B3C8C" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M4 20V10"/><path d="M10 20V4"/><path d="M16 20v-7"/><path d="M22 20H2"/>'
    '</svg></div>'
)

ICONO_DOCUMENTO = (
    '<div style="text-align: center; margin-bottom: 0.5rem;">'
    '<svg xmlns="http://w3.org" width="48" height="48" viewBox="0 0 24 24" fill="none" '
    'stroke="#0B3C8C" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
    '<polyline points="14 2 14 8 20 8"/>'
    '</svg></div>'
)

ICONO_NUBE = (
    '<div style="text-align: center; margin-bottom: 0.5rem;">'
    '<svg xmlns="http://w3.org" width="48" height="48" viewBox="0 0 24 24" fill="none" '
    'stroke="#0B3C8C" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M7 18a4 4 0 0 1-.5-7.97A6 6 0 0 1 18 9.5a4.5 4.5 0 0 1-.5 8.5H7z"/>'
    '</svg></div>'
)

# 2. Menú de navegación lateral con logo
url_logo_estable = "logo.png"
try:
    st.sidebar.image(url_logo_estable, use_container_width=True)
except Exception:
    st.sidebar.markdown("<h3 style='text-align: center;'>🕵️‍♂️</h3>", unsafe_allow_html=True)

st.sidebar.markdown("<hr style='margin-top: 5px; margin-bottom: 5px; border-color: #CBD5E1;'>", unsafe_allow_html=True)
st.sidebar.markdown('<p class="nav-label">Módulos</p>', unsafe_allow_html=True)

ICONOS = {
    "Inicio": ":material/home:",
    "Vigilancia Epidemiológica": ":material/monitoring:",
    "Estadísticas Vitales": ":material/bar_chart:",
    "Boletines Epidemiológicos": ":material/newspaper:",
    "Calendario Epidemiológico 2026": ":material/calendar_month:",
    "Manual de Codificación de EISP": ":material/menu_book:",
}

MODULOS = list(ICONOS.keys())
if "modulo" not in st.session_state:
    st.session_state.modulo = MODULOS[0]

for nombre in MODULOS:
    activo = st.session_state.modulo == nombre
    if st.sidebar.button(
        nombre,
        key=f"btn_{nombre}",
        icon=ICONOS[nombre],
        use_container_width=True,
        type="primary" if activo else "secondary"
    ):
        st.session_state.modulo = nombre
        st.rerun()

opcion = st.session_state.modulo

# 3. Encabezado compacto (solo en los módulos; Inicio tiene su propia portada)
if opcion != "Inicio":
    st.markdown('<h1 class="main-title">Portal de Vigilancia Epidemiológica</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Salud Pública - Departamento del Caquetá</p>', unsafe_allow_html=True)

# 4. Diccionarios de Power BI
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

# Convierte cada página del PDF en imagen
@st.cache_data
def paginas_pdf(ruta):
    import fitz
    doc = fitz.open(ruta)
    return [p.get_pixmap(dpi=150).tobytes("png") for p in doc]

# 5. Lógica de renderizado según la selección del usuario
if opcion == "Inicio":
    st.markdown('<h1 class="hero-title">Portal de Vigilancia Epidemiológica</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Salud Pública — Departamento del Caquetá</p>', unsafe_allow_html=True)
    
    st.markdown(
        '<p class="texto">Este portal reúne la información oficial de vigilancia en salud pública del Departamento del Caquetá: '
        'análisis de eventos de interés notificados al Sivigila, estadísticas de nacimientos y defunciones, boletines epidemiológicos, '
        'el calendario epidemiológico 2026 y el manual de codificación de EISP.</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="texto">Los sistemas interactivos y documentos técnicos se encuentran categorizados y listos para su consulta. '
        'Seleccione el módulo de su interes en el menú lateral para comenzar la navegación.</p>',
        unsafe_allow_html=True
    )
    
    st.write("")
    st.write("")
    
       # 1. Función local automática para codificar las imágenes (Asegúrate de dejarla alineada aquí)
    import base64
    
    def b64_img(ruta_img):
        try:
            with open(ruta_img, "rb") as f:
                return base64.b64encode(f.read()).decode('utf-8')
        except FileNotFoundError:
            return ""

    # 2. Renderizado de Tarjetas Informativas con conversión e Inyección Directa en HTML
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True, key="card_tableros"):
            # Ajusta el tamaño cambiando el width="150px" si lo deseas más grande o pequeño
            st.markdown(f'<div style="text-align: center; margin-bottom: 0.1rem;"><img src="data:image/png;base64,{b64_img("icono1.png")}" width="180px"></div>', unsafe_allow_html=True)
            st.markdown('<div class="card-titulo" style="text-align: center;">Tableros interactivos</div>', unsafe_allow_html=True)
            st.markdown('<p style="color: #4A5568; font-size: 0.95rem; line-height: 1.5; margin: 0; text-align: center;">Módulos dinámicos para filtrar por semana, año y evento epidemiológico directamente en la plataforma con actualizaciones continuas.</p>', unsafe_allow_html=True)
            
    with c2:
        with st.container(border=True, key="card_documentos"):
            st.markdown(f'<div style="text-align: center; margin-bottom: 0.1rem;"><img src="data:image/png;base64,{b64_img("icono2.png")}" width="180px"></div>', unsafe_allow_html=True)
            st.markdown('<div class="card-titulo" style="text-align: center;">Documentos de consulta</div>', unsafe_allow_html=True)
            st.markdown('<p style="color: #4A5568; font-size: 0.95rem; line-height: 1.5; margin: 0; text-align: center;">Acceso integrado en pantalla al calendario epidemiológico anual y al manual de codificación oficial para la correcta gestión de los EISP.</p>', unsafe_allow_html=True)
            
    with c3:
        with st.container(border=True, key="card_boletines"):
            st.markdown(f'<div style="text-align: center; margin-bottom: 0.1rem;"><img src="data:image/png;base64,{b64_img("icono3.png")}" width="180px"></div>', unsafe_allow_html=True)
            st.markdown('<div class="card-titulo" style="text-align: center;">Boletines en la nube</div>', unsafe_allow_html=True)
            st.markdown('<p style="color: #4A5568; font-size: 0.95rem; line-height: 1.5; margin: 0; text-align: center;">Repositorio centralizado ordenado cronológicamente por semanas epidemiológicas enlazado directamente a los servidores institucionales.</p>', unsafe_allow_html=True)

elif opcion == "Boletines Epidemiológicos":
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
    with st.container(height=900):
        for img in paginas_pdf("Codificacion_EISP.pdf"):
            st.image(img, use_container_width=True)
    with open("Codificacion_EISP.pdf", "rb") as f:
        st.download_button(
            "⬇️ Descargar en PDF",
            f,
            file_name="Manual_Codificacion_EISP.pdf",
            mime="application/pdf",
            use_container_width=True
        )

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