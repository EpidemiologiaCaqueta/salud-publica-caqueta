import base64
import streamlit as st
from mapa_municipal import render_mapa

# =====================================================================
# 1. Configuración de la página
# =====================================================================
st.set_page_config(
    page_title="Salud Pública Caquetá",
    page_icon="logo.png",
    layout="wide"
)

# Datos editables del pie de página (si dejas uno vacío, no se muestra)
FUENTES = "Sivigila, RUAF-ND"
ACTUALIZACION = ""   # Ejemplo: "30/09/2026". Vacío = usa la última SE de los datos del mapa
CONTACTO = ""        # Ejemplo: "vigilancia@ejemplo.gov.co"

# Colores institucionales
AZUL = "#0B3C8C"

# =====================================================================
# 2. Estilos
# =====================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=swap');

/* ---------- Base ---------- */
.stApp, .stApp p, .stApp li, .stApp label, .stApp button {
    font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif !important;
}
h1, h2, h3, h4 {
    font-family: 'Poppins', 'Helvetica Neue', Arial, sans-serif !important;
    letter-spacing: -0.01em;
}
[data-testid="stAppViewContainer"] { background: #F4F6FA; }
header[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbarActions"], [data-testid="stDecoration"], #MainMenu { display: none !important; }
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 1.5rem !important;
    max-width: 1480px;
}
[data-testid="stMain"] [data-testid="stVerticalBlock"] { gap: 0.75rem; }

/* Títulos internos de los módulos (st.title / st.subheader) más compactos */
[data-testid="stMain"] [data-testid="stHeading"] h1 { font-size: 1.35rem !important; font-weight: 700 !important; color: #0F2744; padding: 0.2rem 0 !important; }
[data-testid="stMain"] [data-testid="stHeading"] h2 { font-size: 1.2rem !important; color: #0F2744; }
[data-testid="stMain"] [data-testid="stHeading"] h3 { font-size: 1.05rem !important; color: #0F2744; padding: 0.2rem 0 !important; }
[data-testid="stMain"] [data-testid="stHeading"] h4 { font-size: 0.95rem !important; color: #0F2744; }
[data-testid="stCaptionContainer"] { color: #64748B !important; }

/* Botones generales del área principal (descargas, enlaces) */
[data-testid="stMain"] [data-testid="stBaseButton-secondary"] p,
[data-testid="stLinkButton"] a p { font-size: 0.95rem !important; font-weight: 600 !important; }

/* Bordes de contenedores y tableros */
[data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] { border-radius: 12px; }
iframe { border: 1px solid #DCE3EE; border-radius: 12px; background: #FFFFFF; }

/* ---------- Barra lateral ---------- */
[data-testid="stSidebar"], [data-testid="stSidebarContent"] { background: #FFFFFF !important; }
[data-testid="stSidebar"] { border-right: 1px solid #E3E8F0; }
[data-testid="stSidebarHeader"] { height: 0.5rem; padding: 0; }
[data-testid="stSidebarUserContent"] { padding-top: 0.6rem; }
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 0.15rem; }
.side-logo { display: flex; justify-content: center; align-items: center; padding: 0.4rem 0 0.2rem 0; }
.side-logo img { width: 190px; max-width: 85%; height: auto; display: block; }
.nav-label {
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #94A3B8 !important;
    margin: 1rem 0 0.55rem 0.7rem !important;
    line-height: 1.2 !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] { margin-bottom: 0 !important; }
.nav-sep { border: none; border-top: 1px solid #EDF1F6; margin: 0.6rem 0 0 0; }
[data-testid="stSidebar"] button {
    justify-content: flex-start;
    text-align: left;
    border-radius: 8px !important;
    padding: 0.45rem 0.7rem !important;
    min-height: 0 !important;
    transition: background 0.15s ease, color 0.15s ease;
}
[data-testid="stSidebar"] button > div { justify-content: flex-start; width: 100%; }
[data-testid="stSidebar"] button p { font-size: 0.9rem !important; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
[data-testid="stSidebar"] [data-testid="stIconMaterial"] { font-size: 1.15rem !important; }
/* No seleccionado */
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {
    background: transparent !important;
    border: 1px solid transparent !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] p { color: #475569 !important; font-weight: 500; }
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover { background: #F1F5FB !important; }
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover p { color: #0B3C8C !important; }
/* Seleccionado */
[data-testid="stSidebar"] [data-testid="stBaseButton-primary"] {
    background: #EAF1FC !important;
    border: 1px solid #EAF1FC !important;
    box-shadow: inset 3px 0 0 #0B3C8C !important;
}
[data-testid="stSidebar"] [data-testid="stBaseButton-primary"] p { color: #0B3C8C !important; font-weight: 700; }
.side-foot {
    margin: 1.2rem 0.6rem 0 0.6rem;
    padding-top: 0.8rem;
    border-top: 1px solid #EDF1F6;
    font-size: 0.74rem;
    line-height: 1.45;
    color: #94A3B8;
}

/* ---------- Portada ---------- */
.hero {
    position: relative;
    overflow: hidden;
    display: grid;
    grid-template-columns: minmax(0, 1.55fr) minmax(0, 1fr);
    gap: 1.8rem;
    align-items: center;
    background: linear-gradient(125deg, #082D6B 0%, #0B3C8C 45%, #1A5FC0 100%);
    border-radius: 16px;
    padding: 1.9rem 2.1rem;
    box-shadow: 0 12px 30px rgba(8, 45, 107, 0.22);
}
.hero::after {
    content: "";
    position: absolute;
    right: -120px; top: -140px;
    width: 420px; height: 420px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,0.13) 0%, rgba(255,255,255,0) 70%);
    pointer-events: none;
}
.hero-eyebrow {
    color: #A9C4EE !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin: 0 0 0.55rem 0 !important;
}
.hero-title {
    color: #FFFFFF !important;
    font-size: 2.15rem !important;
    font-weight: 800 !important;
    line-height: 1.15 !important;
    padding: 0 !important;
    margin: 0 0 0.6rem 0 !important;
}
.hero-sub {
    color: #DCE7F7 !important;
    font-size: 0.98rem !important;
    line-height: 1.55 !important;
    margin: 0 0 1rem 0 !important;
    max-width: 640px;
}
.hero-meta {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.22);
    border-radius: 999px;
    padding: 0.3rem 0.85rem;
    color: #FFFFFF;
    font-size: 0.8rem;
    font-weight: 500;
}
.hero-meta .punto { width: 7px; height: 7px; border-radius: 50%; background: #4ADE80; box-shadow: 0 0 0 3px rgba(74,222,128,0.25); }
.hero-stats { position: relative; z-index: 1; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0.7rem; }
.stat {
    background: rgba(255,255,255,0.09);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 12px;
    padding: 0.95rem 0.9rem;
    backdrop-filter: blur(4px);
}
.stat-valor {
    font-family: 'Poppins', sans-serif;
    color: #FFFFFF;
    font-size: 1.9rem;
    font-weight: 700;
    line-height: 1;
    font-variant-numeric: tabular-nums;
}
.stat-valor small { font-size: 0.9rem; font-weight: 600; color: #BFD3F3; margin-left: 0.15rem; }
.stat-label { color: #C3D5F2; font-size: 0.75rem; line-height: 1.3; margin-top: 0.4rem; }

.seccion {
    display: flex; align-items: baseline; justify-content: space-between;
    margin: 1.6rem 0 0.35rem 0;
}
.seccion-titulo { font-family: 'Poppins', sans-serif; font-size: 1.02rem; font-weight: 700; color: #0F2744; }
.seccion-nota { font-size: 0.8rem; color: #94A3B8; }

/* Tarjetas de módulos */
[class*="st-key-card_"] {
    background: #FFFFFF;
    border: 1px solid #E3E8F0 !important;
    border-radius: 14px !important;
    box-shadow: 0 1px 2px rgba(15, 39, 68, 0.04);
    padding: 1.15rem 1.2rem 1.1rem 1.2rem !important;
    min-height: 268px !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 0.35rem !important;
    transition: box-shadow 0.2s ease, border-color 0.2s ease, transform 0.2s ease;
}
[class*="st-key-card_"]:hover {
    border-color: #C7D6EE !important;
    box-shadow: 0 10px 24px rgba(11, 60, 140, 0.10);
    transform: translateY(-2px);
}
[class*="st-key-card_"] > [data-testid="stElementContainer"]:last-child { margin-top: auto; }
.tile-head { display: flex; align-items: flex-start; justify-content: space-between; }
.tile-icon {
    width: 76px; height: 76px;
    border-radius: 16px;
    background: #EEF4FC;
    border: 1px solid #DCE7F7;
    overflow: hidden;
    display: flex; align-items: center; justify-content: center;
}
.tile-icon img { width: 70px; height: 70px; object-fit: contain; transform: scale(1.18); }
.tile-tag {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase;
    color: #0B3C8C; background: #EAF1FC; border-radius: 6px; padding: 0.2rem 0.5rem;
}
.tile-title { font-family: 'Poppins', sans-serif; font-size: 1.02rem; font-weight: 700; color: #0F2744; margin: 0.8rem 0 0.25rem 0; }
.tile-desc { color: #64748B !important; font-size: 0.86rem !important; line-height: 1.5 !important; margin: 0 !important; }
[class*="st-key-card_"] [data-testid="stBaseButton-secondary"] {
    background: #FFFFFF !important;
    border: 1px solid #D5DFEE !important;
    border-radius: 9px !important;
    min-height: 0 !important;
    padding: 0.4rem 0.8rem !important;
}
[data-testid="stMain"] [class*="st-key-card_"] [data-testid="stBaseButton-secondary"] p {
    font-size: 0.85rem !important; font-weight: 600 !important; color: #0B3C8C !important;
}
[class*="st-key-card_"] [data-testid="stBaseButton-secondary"]:hover { background: #0B3C8C !important; border-color: #0B3C8C !important; }
[class*="st-key-card_"] [data-testid="stBaseButton-secondary"]:hover p { color: #FFFFFF !important; }

/* ---------- Encabezado de los módulos ---------- */
.page-head {
    background: #FFFFFF;
    border: 1px solid #E3E8F0;
    border-left: 4px solid #0B3C8C;
    border-radius: 12px;
    padding: 0.85rem 1.2rem;
    margin-bottom: 0.4rem;
}
.crumb { font-size: 0.74rem; color: #94A3B8; font-weight: 500; margin-bottom: 0.15rem; }
.crumb b { color: #0B3C8C; font-weight: 600; }
.page-title { font-family: 'Poppins', sans-serif; font-size: 1.4rem; font-weight: 700; color: #0F2744; line-height: 1.25; }
.page-desc { font-size: 0.88rem; color: #64748B; margin-top: 0.15rem; }

/* ---------- Paneles de los módulos ---------- */
[class*="st-key-panel_"] {
    background: #FFFFFF;
    border: 1px solid #E3E8F0;
    border-radius: 12px;
    padding: 1rem 1.15rem !important;
    gap: 0.6rem !important;
}
.panel-titulo { font-family: 'Poppins', sans-serif; font-size: 0.98rem; font-weight: 700; color: #0F2744; }
.panel-sub { font-size: 0.8rem; color: #94A3B8; }
.panel-texto { color: #64748B !important; font-size: 0.86rem !important; line-height: 1.55 !important; margin: 0.9rem 0 0.9rem 0 !important; }
[class*="st-key-panel_"] [data-testid="stDownloadButton"],
[class*="st-key-panel_"] [data-testid="stLinkButton"] { margin-top: 0.15rem; }
.portada-pdf { display: flex; justify-content: center; }
.portada-pdf img {
    width: 100%; max-width: 230px; border-radius: 6px;
    border: 1px solid #E3E8F0; box-shadow: 0 8px 22px rgba(15, 39, 68, 0.12);
}
.portada-nota { text-align: center; font-size: 0.75rem; color: #94A3B8; margin-top: 0.5rem; }
.bol-head { display: flex; align-items: center; gap: 0.9rem; }
.lista-check { margin-top: 0.5rem; }
.lista-check div {
    display: flex; gap: 0.6rem; align-items: flex-start;
    padding: 0.5rem 0; border-bottom: 1px solid #EEF2F7;
    font-size: 0.86rem; color: #475569;
}
.lista-check div:last-child { border-bottom: none; }
.ok { color: #16A34A; font-weight: 700; }
.se-actual {
    background: linear-gradient(125deg, #082D6B 0%, #0B3C8C 55%, #1A5FC0 100%);
    border-radius: 12px; padding: 1rem 1.1rem; color: #FFFFFF;
}
.se-label { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #A9C4EE; }
.se-num { font-family: 'Poppins', sans-serif; font-size: 2.2rem; font-weight: 700; line-height: 1.1; margin-top: 0.2rem; }
.se-fechas { font-size: 0.85rem; color: #DCE7F7; }
.resumen-lat { margin: 0.7rem 0 0.4rem 0; border-top: 1px solid #EEF2F7; }
.resumen-lat div { display: flex; justify-content: space-between; padding: 0.45rem 0; border-bottom: 1px solid #EEF2F7; font-size: 0.85rem; }
.resumen-lat span { color: #64748B; }
.resumen-lat b { color: #0F2744; font-weight: 600; }
[class*="st-key-panel_"] [data-testid="stBaseButton-primary"],
[class*="st-key-panel_"] [data-testid="stBaseLinkButton-primary"] {
    background: #0B3C8C !important; border-color: #0B3C8C !important; border-radius: 9px !important;
}
[class*="st-key-panel_"] [data-testid="stBaseButton-primary"] p,
[class*="st-key-panel_"] [data-testid="stBaseLinkButton-primary"] p { color: #FFFFFF !important; }

/* Botones compactos dentro de los paneles */
[class*="st-key-panel_"] [data-testid="stBaseButton-primary"],
[class*="st-key-panel_"] [data-testid="stBaseLinkButton-primary"],
[class*="st-key-panel_"] [data-testid="stBaseLinkButton-secondary"] {
    min-height: 0 !important;
    padding: 0.4rem 1rem !important;
    width: auto !important;
}
[data-testid="stMain"] [class*="st-key-panel_"] button p,
[data-testid="stMain"] [class*="st-key-panel_"] a p { font-size: 0.85rem !important; font-weight: 600 !important; }
[class*="st-key-panel_powerbi"] [data-testid="stLinkButton"] { display: flex; justify-content: flex-end; }

/* Ícono del módulo activo visible en el menú */
[data-testid="stSidebar"] [data-testid="stBaseButton-primary"] [data-testid="stIconMaterial"] { color: #0B3C8C !important; }
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] [data-testid="stIconMaterial"] { color: #64748B !important; }

/* ---------- Pie de página ---------- */
.pie {
    margin-top: 1.6rem;
    background: #0A2350;
    border-radius: 14px;
    padding: 1.2rem 1.5rem 0.9rem 1.5rem;
    color: #B8C8E2;
    font-size: 0.82rem;
}
.pie-fila { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 0.8rem 2rem; }
.pie-marca { font-family: 'Poppins', sans-serif; color: #FFFFFF; font-weight: 700; font-size: 0.95rem; }
.pie-entidad { color: #9FB3D6; font-size: 0.8rem; margin-top: 0.1rem; }
.pie-datos { display: flex; flex-wrap: wrap; gap: 0.4rem 1.6rem; }
.pie-datos span { color: #B8C8E2; }
.pie-datos b { color: #FFFFFF; font-weight: 600; }
.pie-legal {
    margin-top: 0.85rem; padding-top: 0.7rem;
    border-top: 1px solid rgba(255,255,255,0.10);
    font-size: 0.74rem; color: #7F94BA;
}

/* ---------- Celulares ---------- */
@media (max-width: 900px) {
    .hero { grid-template-columns: 1fr; padding: 1.4rem 1.3rem; gap: 1.1rem; }
    .hero-title { font-size: 1.6rem !important; }
    .stat-valor { font-size: 1.45rem; }
}
@media (max-width: 768px) {
    [data-testid="stHorizontalBlock"] { flex-direction: column !important; gap: 0.8rem !important; }
    [class*="st-key-card_"] { min-height: auto !important; }
    .block-container { padding-top: 3.2rem !important; }
}
</style>
""", unsafe_allow_html=True)


# =====================================================================
# 3. Utilidades
# =====================================================================
@st.cache_data
def b64_img(ruta_img):
    try:
        with open(ruta_img, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError:
        return ""


@st.cache_data
def resumen_datos(version_datos=None):
    """Resumen automático de casos_municipio.csv (portada y pie de página)."""
    try:
        import pandas as pd
        d = pd.read_csv("casos_municipio.csv", dtype={"evento": str})
        anio = int(d["anio"].max())
        d = d[d["anio"] == anio]
        return {
            "eventos": d["evento"].nunique(),
            "anio": anio,
            "semana": int(d["semana"].max()),
            "casos": int(d["casos"].sum()),
        }
    except Exception:
        return None


@st.cache_data
def portada_pdf(ruta):
    """Imagen de la primera página del PDF y número total de páginas."""
    try:
        import fitz
        doc = fitz.open(ruta)
        return doc[0].get_pixmap(dpi=90).tobytes("png"), len(doc)
    except Exception:
        return None, None


@st.cache_data
def paginas_pdf(ruta):
    """Convierte cada página del PDF en imagen."""
    import fitz
    doc = fitz.open(ruta)
    return [p.get_pixmap(dpi=150).tobytes("png") for p in doc]


def ir_a(modulo):
    st.session_state.modulo = modulo


import os
RESUMEN = resumen_datos(os.path.getmtime("casos_municipio.csv") if os.path.exists("casos_municipio.csv") else None)

# =====================================================================
# 4. Menú lateral
# =====================================================================
st.sidebar.markdown(
    f'<div class="side-logo"><img src="data:image/png;base64,{b64_img("logo.png")}" alt="Vigilancia Epidemiológica"></div>'
    '<hr class="nav-sep">',
    unsafe_allow_html=True
)

ICONOS = {
    "Inicio": ":material/home:",
    "Vigilancia Epidemiológica": ":material/monitoring:",
    "Estadísticas Vitales": ":material/bar_chart:",
    "Georreferenciación de EISP": ":material/map:",
    "Boletines Epidemiológicos": ":material/newspaper:",
    "Calendario Epidemiológico 2026": ":material/calendar_month:",
    "Manual de Codificación de EISP": ":material/menu_book:",
}

DESCRIPCIONES = {
    "Vigilancia Epidemiológica": "Análisis de los eventos de interés en salud pública notificados al Sivigila.",
    "Estadísticas Vitales": "Cifras de nacimientos y defunciones del departamento.",
    "Georreferenciación de EISP": "Casos por municipio con filtros por evento, año y semana epidemiológica.",
    "Boletines Epidemiológicos": "Histórico de boletines organizados por semana epidemiológica (SE).",
    "Calendario Epidemiológico 2026": "Semanas epidemiológicas oficiales del año 2026.",
    "Manual de Codificación de EISP": "Guía oficial de codificación de los eventos de interés en salud pública.",
}

MODULOS = list(ICONOS.keys())
if "modulo" not in st.session_state:
    st.session_state.modulo = MODULOS[0]

# Nombres cortos para el menú (el nombre completo se ve en el encabezado del módulo)
ETIQUETAS = {
    "Inicio": "Inicio",
    "Vigilancia Epidemiológica": "Eventos de interés (EISP)",
    "Estadísticas Vitales": "Estadísticas vitales",
    "Georreferenciación de EISP": "Georreferenciación",
    "Boletines Epidemiológicos": "Boletines",
    "Calendario Epidemiológico 2026": "Calendario 2026",
    "Manual de Codificación de EISP": "Manual de codificación",
}
GRUPOS = [
    ("General", ["Inicio"]),
    ("Análisis", ["Vigilancia Epidemiológica", "Estadísticas Vitales", "Georreferenciación de EISP"]),
    ("Documentos", ["Boletines Epidemiológicos", "Calendario Epidemiológico 2026", "Manual de Codificación de EISP"]),
]

for grupo, nombres in GRUPOS:
    st.sidebar.markdown(f'<p class="nav-label">{grupo}</p>', unsafe_allow_html=True)
    for nombre in nombres:
        st.sidebar.button(
            ETIQUETAS[nombre],
            key=f"btn_{nombre}",
            icon=ICONOS[nombre],
            use_container_width=True,
            type="primary" if st.session_state.modulo == nombre else "secondary",
            on_click=ir_a,
            args=(nombre,),
        )

st.sidebar.markdown(
    '<div class="side-foot">Área de Vigilancia Epidemiológica<br>'
    'Secretaría de Salud Departamental del Caquetá</div>',
    unsafe_allow_html=True
)

opcion = st.session_state.modulo

# Encabezado compacto de cada módulo (Inicio tiene su propia portada)
if opcion not in ("Inicio", "Vigilancia Epidemiológica"):
    st.markdown(
        '<div class="page-head">'
        f'<div class="page-title">{opcion}</div>'
        f'<div class="page-desc">{DESCRIPCIONES.get(opcion, "")}</div>'
        '</div>',
        unsafe_allow_html=True
    )

# =====================================================================
# 5. Tableros de Power BI
# =====================================================================
urls_powerbi = {
    "Vigilancia Epidemiológica": "https://app.powerbi.com/view?r=eyJrIjoiYzFiOTAwMzQtN2VkNy00NDhiLThjMTItZGY3NzNhMjExMTkwIiwidCI6IjkxOTM0N2Q1LTkyMWUtNDczOC05MGJkLTJkMTU4YzUzM2QzOCIsImMiOjR9",
    "Estadísticas Vitales": "https://app.powerbi.com/view?r=eyJrIjoiNTZiZjhlMzQtOTgxNS00MDUwLTlkMjMtMDQ2OWI3ZjA5YjU0IiwidCI6IjkxOTM0N2Q1LTkyMWUtNDczOC05MGJkLTJkMTU4YzUzM2QzOCIsImMiOjR9"
}
alturas_powerbi = {
    "Vigilancia Epidemiológica": 900,
    "Estadísticas Vitales": 1670
}

# =====================================================================
# 6. Contenido de cada módulo
# =====================================================================
if opcion == "Inicio":
    # ---- Banner con indicadores ----
    if RESUMEN:
        meta = f'<span class="punto"></span>Datos actualizados a la SE {RESUMEN["semana"]} de {RESUMEN["anio"]}'
        stats = (
            f'<div class="stat"><div class="stat-valor">{RESUMEN["eventos"]}</div><div class="stat-label">Eventos georreferenciados</div></div>'
            f'<div class="stat"><div class="stat-valor">{RESUMEN["semana"]}<small>SE</small></div><div class="stat-label">Última semana epidemiológica</div></div>'
            '<div class="stat"><div class="stat-valor">16</div><div class="stat-label">Municipios del Caquetá</div></div>'
        )
    else:
        meta = '<span class="punto"></span>Información oficial del departamento'
        stats = '<div class="stat"><div class="stat-valor">16</div><div class="stat-label">Municipios del Caquetá</div></div>'

    st.markdown(
        '<div class="hero">'
        '<div style="position: relative; z-index: 1;">'
        '<p class="hero-eyebrow">Secretaría de Salud Departamental del Caquetá</p>'
        '<h1 class="hero-title">Portal de Vigilancia Epidemiológica</h1>'
        '<p class="hero-sub">Información oficial de vigilancia en salud pública del Caquetá: eventos de interés '
        'notificados al Sivigila, estadísticas vitales, georreferenciación, boletines y documentos técnicos.</p>'
        f'<div class="hero-meta">{meta}</div>'
        '</div>'
        f'<div class="hero-stats">{stats}</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # ---- Accesos directos ----
    st.markdown(
        '<div class="seccion"><span class="seccion-titulo">Módulos del portal</span>'
        '<span class="seccion-nota">Seleccione un módulo para comenzar</span></div>',
        unsafe_allow_html=True
    )

    TARJETAS = [
        ("tableros", "icono1.png", "Interactivo", "Tableros interactivos",
         "Filtros por semana, año y evento epidemiológico con actualización continua.",
         "Vigilancia Epidemiológica"),
        ("georreferenciacion", "icono4.png", "Mapas", "Georreferenciación",
         "Casos por municipio de los eventos de interés en salud pública del Caquetá.",
         "Georreferenciación de EISP"),
        ("boletines", "icono3.png", "Repositorio", "Boletines epidemiológicos",
         "Histórico ordenado por semanas epidemiológicas, disponible en la nube.",
         "Boletines Epidemiológicos"),
        ("documentos", "icono2.png", "Documentos", "Documentos de consulta",
         "Calendario epidemiológico anual y manual oficial de codificación de EISP.",
         "Calendario Epidemiológico 2026"),
    ]

    columnas = st.columns(4)
    for col, (clave, img, tag, titulo, desc, destino) in zip(columnas, TARJETAS):
        with col:
            with st.container(key=f"card_{clave}"):
                st.markdown(
                    '<div class="tile-head">'
                    f'<div class="tile-icon"><img src="data:image/png;base64,{b64_img(img)}"></div>'
                    f'<span class="tile-tag">{tag}</span>'
                    '</div>'
                    f'<div class="tile-title">{titulo}</div>'
                    f'<p class="tile-desc">{desc}</p>',
                    unsafe_allow_html=True
                )
                st.button(
                    "Abrir módulo",
                    key=f"ir_{clave}",
                    icon=":material/arrow_forward:",
                    on_click=ir_a,
                    args=(destino,),
                    use_container_width=True,
                )

elif opcion == "Georreferenciación de EISP":
    render_mapa()

elif opcion == "Boletines Epidemiológicos":
    URL_BOLETINES = "https://drive.google.com/drive/folders/1tUQdlVhytJqKxA6-tBK4Yw7pThfy-X0h?usp=sharing"
    with st.container(key="panel_boletines"):
        c1, c2 = st.columns([1.5, 1], gap="large")
        with c1:
            st.markdown(
                '<div class="bol-head">'
                f'<div class="tile-icon"><img src="data:image/png;base64,{b64_img("icono3.png")}"></div>'
                '<div><div class="panel-titulo">Repositorio oficial de boletines</div>'
                '<div class="panel-sub">Carpeta pública en Google Drive</div></div>'
                '</div>'
                '<p class="panel-texto">Consulte cada boletín en línea o descárguelo en PDF. Las carpetas están ordenadas de la semana más reciente a la más antigua.</p>',
                unsafe_allow_html=True
            )
            st.link_button(
                "Abrir boletines",
                URL_BOLETINES,
                icon=":material/open_in_new:",
                type="primary",
            )
        with c2:
            st.markdown(
                '<div class="lista-check">'
                '<div><span class="ok">✓</span>Acceso público, sin usuario ni contraseña</div>'
                '<div><span class="ok">✓</span>Ordenados cronológicamente por SE</div>'
                '<div><span class="ok">✓</span>Formato PDF, desde cualquier dispositivo</div>'
                '<div><span class="ok">✓</span>Se abre en una pestaña nueva</div>'
                '</div>',
                unsafe_allow_html=True
            )

elif opcion == "Calendario Epidemiológico 2026":
    import datetime as dt
    try:
        from zoneinfo import ZoneInfo
        hoy = dt.datetime.now(ZoneInfo("America/Bogota")).date()
    except Exception:
        hoy = dt.date.today()

    def inicio_se1(anio):
        """Domingo en que inicia la SE 1 (semana con al menos 4 días del año)."""
        enero4 = dt.date(anio, 1, 4)
        return enero4 - dt.timedelta(days=(enero4.weekday() + 1) % 7)

    inicio = inicio_se1(hoy.year)
    if hoy < inicio:
        inicio = inicio_se1(hoy.year - 1)
    se_actual = (hoy - inicio).days // 7 + 1
    ini_se = inicio + dt.timedelta(weeks=se_actual - 1)
    fin_se = ini_se + dt.timedelta(days=6)
    meses = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
    fecha = lambda f: f"{f.day} {meses[f.month - 1]}"

    c1, c2 = st.columns([2.1, 1], gap="small")
    with c1:
        with st.container(key="panel_calendario"):
            st.image("Calendario2026.png", use_container_width=True)
    with c2:
        with st.container(key="panel_cal_info"):
            st.markdown(
                '<div class="se-actual">'
                '<div class="se-label">Semana epidemiológica actual</div>'
                f'<div class="se-num">SE {se_actual}</div>'
                f'<div class="se-fechas">{fecha(ini_se)} – {fecha(fin_se)} de {fin_se.year}</div>'
                '</div>'
                '<div class="lista-check">'
                '<div><span class="ok">✓</span>Las semanas inician el domingo y terminan el sábado</div>'
                '<div><span class="ok">✓</span>Base para la notificación semanal al Sivigila</div>'
                '<div><span class="ok">✓</span>Calendario oficial del año 2026</div>'
                '</div>',
                unsafe_allow_html=True
            )
            with open("Calendario2026.pdf", "rb") as f:
                st.download_button(
                    "Descargar PDF",
                    f,
                    file_name="calendario_epidemiologico_2026.pdf",
                    mime="application/pdf",
                    icon=":material/download:",
                    type="primary",
                )

elif opcion == "Manual de Codificación de EISP":
    import os
    peso = os.path.getsize("Codificacion_EISP.pdf") / 1024
    portada, n_paginas = portada_pdf("Codificacion_EISP.pdf")
    with st.container(key="panel_manual"):
        c1, c2 = st.columns([1.5, 1], gap="large")
        with c1:
            detalle = f"PDF · {peso:,.0f} KB".replace(",", ".")
            if n_paginas:
                detalle += f" · {n_paginas} páginas"
            st.markdown(
                '<div class="bol-head">'
                f'<div class="tile-icon"><img src="data:image/png;base64,{b64_img("icono2.png")}"></div>'
                '<div><div class="panel-titulo">Documento completo</div>'
                f'<div class="panel-sub">{detalle}</div></div>'
                '</div>'
                '<p class="panel-texto">Descargue el manual para consultarlo en su equipo, incluso sin conexión. '
                'Contiene los códigos y criterios para registrar correctamente cada evento.</p>',
                unsafe_allow_html=True
            )
            with open("Codificacion_EISP.pdf", "rb") as f:
                st.download_button(
                    "Descargar PDF",
                    f,
                    file_name="Manual_Codificacion_EISP.pdf",
                    mime="application/pdf",
                    icon=":material/download:",
                    type="primary",
                )
        with c2:
            if portada:
                b64 = base64.b64encode(portada).decode("utf-8")
                st.markdown(
                    f'<div class="portada-pdf"><img src="data:image/png;base64,{b64}" alt="Portada del manual"></div>'
                    '<div class="portada-nota">Vista previa de la portada</div>',
                    unsafe_allow_html=True
                )

elif opcion == "Estadísticas Vitales":
    from pathlib import Path
    st.iframe(Path(__file__).parent / "tablero_estadisticas_vitales.html", height=1400)

elif opcion == "Vigilancia Epidemiológica":
    from pathlib import Path
    # Tablero a pantalla completa: sin márgenes y alto = alto de la ventana
    st.markdown("""<style>
.block-container { padding: 0.5rem 0.6rem 0 0.6rem !important; max-width: none !important; }
header[data-testid="stHeader"] { pointer-events: none; }
header[data-testid="stHeader"] button { pointer-events: auto; }
iframe.stIFrame { height: calc(100vh - 1.4rem) !important; display: block; border-radius: 10px; }
</style>""", unsafe_allow_html=True)
    st.iframe(Path(__file__).parent / "tablero_eisp.html", height=900)

else:
    with st.container(key="panel_powerbi"):
        h1, h2 = st.columns([4, 1], vertical_alignment="center")
        h1.markdown(
            '<div class="panel-titulo">Tablero interactivo</div>'
            '<div class="panel-sub">Use los filtros del tablero para consultar por año, semana, evento y municipio.</div>',
            unsafe_allow_html=True
        )
        h2.link_button("Pantalla completa", urls_powerbi[opcion], icon=":material/open_in_full:")
        st.iframe(urls_powerbi[opcion], height=alturas_powerbi[opcion])

# =====================================================================
# 7. Pie de página institucional
# =====================================================================
datos_pie = [f"<span><b>Fuentes:</b> {FUENTES}</span>"]
if ACTUALIZACION:
    datos_pie.append(f"<span><b>Última actualización:</b> {ACTUALIZACION}</span>")
elif RESUMEN:
    datos_pie.append(f"<span><b>Datos hasta:</b> SE {RESUMEN['semana']} de {RESUMEN['anio']}</span>")
if CONTACTO:
    datos_pie.append(f"<span><b>Contacto:</b> {CONTACTO}</span>")

st.markdown(
    '<div class="pie">'
    '<div class="pie-fila">'
    '<div><div class="pie-marca">Portal de Vigilancia Epidemiológica</div>'
    '<div class="pie-entidad">Área de Vigilancia Epidemiológica · Secretaría de Salud Departamental del Caquetá</div></div>'
    f'<div class="pie-datos">{"".join(datos_pie)}</div>'
    '</div>'
    '<div class="pie-legal">© 2026 Área de Vigilancia Epidemiológica - Departamento del Caquetá. '
    'Información para uso estrictamente informativo y estadístico.</div>'
    '</div>',
    unsafe_allow_html=True
)
