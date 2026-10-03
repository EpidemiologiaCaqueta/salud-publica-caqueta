"""Módulo Streamlit: mapa de casos por municipio - Caquetá.

Archivos necesarios en el repositorio (misma carpeta que este archivo):
  - caqueta_municipios.geojson   (lo genera preparar_datos_mapa.py, paso 1)
  - casos_municipio.csv          (lo genera preparar_datos_mapa.py, paso 2)
  - poblacion_municipios.csv     (OPCIONAL, para tasas: columnas cod_mun, poblacion)
"""
import json
import os

import pandas as pd
import plotly.express as px
import streamlit as st

GEOJSON = "caqueta_municipios.geojson"
DATOS = "casos_municipio.csv"
POBLACION = "poblacion_municipios.csv"

# Nombres de eventos para mostrar en el selector (VERIFICA contra el protocolo/INS)
NOMBRES_EVENTO = {
    "100": "100 - Accidente ofídico",
    "113": "113 - Desnutrición aguda en menores de 5 años",
    "210": "210 - Dengue",
    "330": "330 - Hepatitis A",
    "356": "356 - Intento de suicidio",
    "450": "450 - Intoxicaciones por sustancias químicas",
    "591": "591 - COVID-19",
    "730": "730 - Sarampión / Rubéola",
    "813": "813 - Tuberculosis",
    "880": "880 - Mpox",
}


@st.cache_data
def cargar_datos(version_datos):
    # version_datos (fecha de modificación del CSV) hace que el caché se renueve
    # solo cuando cambias casos_municipio.csv.
    with open(GEOJSON, encoding="utf-8") as f:
        geo = json.load(f)
    base = pd.DataFrame(
        [
            {
                "cod_mun": ft["properties"]["cod_mun"],
                "municipio": ft["properties"]["municipio"],
            }
            for ft in geo["features"]
        ]
    )
    datos = pd.read_csv(DATOS, dtype={"cod_mun": str, "evento": str})
    poblacion = None
    if os.path.exists(POBLACION):
        poblacion = pd.read_csv(POBLACION, dtype={"cod_mun": str})
    return geo, base, datos, poblacion


def render_mapa():
    st.title("Mapa de casos por municipio - Caquetá")
    geo, base, datos, poblacion = cargar_datos(os.path.getmtime(DATOS))

    # ---- Filtros
    c1, c2 = st.columns(2)
    eventos = sorted(datos["evento"].unique())
    evento = c1.selectbox(
        "Evento", eventos, format_func=lambda e: NOMBRES_EVENTO.get(e, e)
    )
    anios = sorted(datos["anio"].unique(), reverse=True)
    anio = c2.selectbox("Año", anios)

    sub = datos[(datos["evento"] == evento) & (datos["anio"] == anio)]
    sem_min, sem_max = int(datos["semana"].min()), int(datos["semana"].max())
    sem_ini, sem_fin = st.slider(
        "Semanas epidemiológicas", sem_min, sem_max, (sem_min, sem_max)
    )
    sub = sub[(sub["semana"] >= sem_ini) & (sub["semana"] <= sem_fin)]

    opciones = ["Casos"]
    if poblacion is not None:
        opciones.append("Tasa por 100.000 habitantes")
    indicador = st.radio("Indicador", opciones, horizontal=True)

    # ---- Agregación (todos los municipios, incluso con 0 casos)
    agg = sub.groupby("cod_mun", as_index=False)["casos"].sum()
    df = base.merge(agg, on="cod_mun", how="left").fillna({"casos": 0})
    df["casos"] = df["casos"].astype(int)

    es_tasa = indicador.startswith("Tasa")
    if es_tasa:
        df = df.merge(poblacion[["cod_mun", "poblacion"]], on="cod_mun", how="left")
        df["valor"] = (df["casos"] / df["poblacion"] * 100000).round(1)
        etiqueta = "Tasa x 100.000"
    else:
        df["valor"] = df["casos"]
        etiqueta = "Casos"

    st.metric("Total de casos en el departamento", int(df["casos"].sum()))

    # ---- Mapa
    kwargs = dict(
        data_frame=df,
        geojson=geo,
        locations="cod_mun",
        featureidkey="properties.cod_mun",
        color="valor",
        color_continuous_scale="YlOrRd",
        hover_name="municipio",
        hover_data={"cod_mun": False, "casos": True, "valor": True},
        labels={"valor": etiqueta, "casos": "Casos"},
        zoom=6,
        center={"lat": 1.0, "lon": -74.0},
        opacity=0.8,
    )
    if hasattr(px, "choropleth_map"):  # plotly >= 5.24
        fig = px.choropleth_map(map_style="carto-positron", **kwargs)
    else:
        fig = px.choropleth_mapbox(mapbox_style="carto-positron", **kwargs)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=600)
    st.plotly_chart(fig, use_container_width=True)

    # ---- Tabla
    st.subheader(f"{NOMBRES_EVENTO.get(evento, evento)} · {anio} · SE {sem_ini}-{sem_fin}")
    cols = ["municipio", "casos"] + (["valor"] if es_tasa else [])
    st.dataframe(
        df.sort_values("valor", ascending=False)[cols].rename(columns={"valor": etiqueta}),
        hide_index=True,
        use_container_width=True,
    )
    st.caption("Fuente: SIVIGILA. Datos agregados por municipio de procedencia.")
    if es_tasa:
        st.caption(
            "La tasa usa la población DANE del municipio; al contar casos por "
            "procedencia, interprétala con cautela."
        )