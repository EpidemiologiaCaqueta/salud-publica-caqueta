"""Módulo Streamlit: mapa de casos por municipio - Caquetá."""

import json
import os

import pandas as pd
import plotly.express as px
import streamlit as st


GEOJSON = "caqueta_municipios.geojson"
DATOS = "casos_municipio.csv"
POBLACION = "poblacion_municipios.csv"

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
    with open(GEOJSON, encoding="utf-8") as f:
        geo = json.load(f)

    base = pd.DataFrame(
        [
            {
                "cod_mun": str(ft["properties"]["cod_mun"]),
                "municipio": ft["properties"]["municipio"],
            }
            for ft in geo["features"]
        ]
    )

    datos = pd.read_csv(
        DATOS,
        dtype={"cod_mun": str, "evento": str}
    )

    poblacion = None
    if os.path.exists(POBLACION):
        poblacion = pd.read_csv(
            POBLACION,
            dtype={"cod_mun": str}
        )

    return geo, base, datos, poblacion


def render_mapa():
    st.title("Mapa de casos por municipio - Caquetá")

    geo, base, datos, poblacion = cargar_datos(
        os.path.getmtime(DATOS)
    )

   
    # ---- Panel profesional de filtros
    
    st.markdown("#### Filtros de consulta")

    # Primera fila: evento y año
    c1, c2 = st.columns(2)

    eventos = sorted(datos["evento"].unique())

    evento = c1.selectbox(
        "Evento epidemiológico",
        eventos,
        format_func=lambda e: NOMBRES_EVENTO.get(e, e),
    )

    anios = sorted(datos["anio"].unique(), reverse=True)

    anio = c2.selectbox(
        "Año",
        anios,
    )

    # Filtrar evento y año
    sub = datos[
        (datos["evento"] == evento)
        & (datos["anio"] == anio)
    ].copy()

    if sub.empty:
        st.warning("No hay registros para el evento y año seleccionados.")
        return

    # Rango de semanas disponible para el evento y año seleccionados
    sem_min = int(sub["semana"].min())
    sem_max = int(sub["semana"].max())

    if sem_min == sem_max:
        sem_ini, sem_fin = sem_min, sem_max
        st.info(f"Semana epidemiológica disponible: {sem_min}")
    else:
        sem_ini, sem_fin = st.slider(
            "Semana epidemiológica",
            min_value=sem_min,
            max_value=sem_max,
            value=(sem_min, sem_max),
            help="Selecciona el rango de semanas que deseas consultar.",
        )

    sub = sub[
        (sub["semana"] >= sem_ini)
        & (sub["semana"] <= sem_fin)
    ].copy()

    # Segunda fila: municipio e indicador
    c3, c4 = st.columns(2)

    municipios = [
        "Todos los municipios"
    ] + sorted(base["municipio"].dropna().unique().tolist())

    municipio_seleccionado = c3.selectbox(
        "Municipio",
        municipios,
    )

    opciones = ["Casos"]

    if poblacion is not None:
        opciones.append("Tasa por 100.000 habitantes")

    indicador = c4.radio(
        "Indicador",
        opciones,
        horizontal=True,
    )

    # Agregación por municipio
    agg = sub.groupby(
        "cod_mun",
        as_index=False
    )["casos"].sum()

    df = base.merge(
        agg,
        on="cod_mun",
        how="left"
    )

    df["casos"] = df["casos"].fillna(0).astype(int)

    es_tasa = indicador.startswith("Tasa")

    if es_tasa:
        df = df.merge(
            poblacion[["cod_mun", "poblacion"]],
            on="cod_mun",
            how="left"
        )

        df["valor"] = (
            df["casos"] / df["poblacion"] * 100000
        ).round(1)

        etiqueta = "Tasa x 100.000"
    else:
        df["valor"] = df["casos"]
        etiqueta = "Casos"

    # Aplicar filtro de municipio
    if municipio_seleccionado != "Todos los municipios":
        df = df[
            df["municipio"] == municipio_seleccionado
        ].copy()

        st.metric(
            f"Total de casos en {municipio_seleccionado}",
            int(df["casos"].sum())
        )
    else:
        st.metric(
            "Total de casos en el departamento",
            int(df["casos"].sum())
        )

    # Mapa
    kwargs = dict(
        data_frame=df,
        geojson=geo,
        locations="cod_mun",
        featureidkey="properties.cod_mun",
        color="valor",
        color_continuous_scale="YlOrRd",
        hover_name="municipio",
        hover_data={
            "cod_mun": False,
            "casos": True,
            "valor": True,
        },
        labels={
            "valor": etiqueta,
            "casos": "Casos",
        },
        zoom=6,
        center={"lat": 1.0, "lon": -74.0},
        opacity=0.8,
    )

    if hasattr(px, "choropleth_map"):
        fig = px.choropleth_map(
            map_style="carto-positron",
            **kwargs
        )
    else:
        fig = px.choropleth_mapbox(
            mapbox_style="carto-positron",
            **kwargs
        )

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=600
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Tabla
    st.subheader(
        f"{NOMBRES_EVENTO.get(evento, evento)} · "
        f"{anio} · SE {sem_ini}-{sem_fin}"
    )

    cols = ["municipio", "casos"]

    if es_tasa:
        cols.append("valor")

    tabla = df.sort_values(
        "valor",
        ascending=False
    )[cols].rename(
        columns={"valor": etiqueta}
    )

    st.dataframe(
        tabla,
        hide_index=True,
        use_container_width=True
    )

    st.caption(
        "Fuente: SIVIGILA. Datos agregados por municipio de procedencia."
    )

    if es_tasa:
        st.caption(
            "La tasa usa la población DANE del municipio; al contar "
            "casos por procedencia, interprétala con cautela."
        )


if __name__ == "__main__":
    render_mapa()