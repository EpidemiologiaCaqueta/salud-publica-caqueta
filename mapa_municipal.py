"""Módulo Streamlit: georreferenciación de casos por municipio - Caquetá."""

import json
import os
import pandas as pd
import plotly.express as px
import streamlit as st


GEOJSON = "caqueta_municipios.geojson"
DATOS = "casos_municipio.csv"
POBLACION = "poblacion_municipios.csv"

AZUL = "#0B3C8C"
ESCALA = ["#FFF5EB", "#FDD0A2", "#FD8D3C", "#E6550D", "#A63603"]

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

ESTILOS = """
<style>
/* Barra de filtros */
.st-key-geo_filtros {
    background: #FFFFFF;
    border: 1px solid #E3E8F0;
    border-radius: 12px;
    padding: 0.8rem 1rem 0.3rem 1rem !important;
}
.st-key-geo_filtros label p { font-size: 0.78rem !important; font-weight: 600 !important; color: #475569 !important; }

/* Indicadores */
.kpis { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0.75rem; }
.kpi {
    background: #FFFFFF;
    border: 1px solid #E3E8F0;
    border-radius: 12px;
    padding: 0.8rem 1rem;
}
.kpi-label { font-size: 0.72rem; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; color: #94A3B8; }
.kpi-valor {
    font-family: 'Poppins', sans-serif; font-size: 1.6rem; font-weight: 700; color: #0F2744;
    line-height: 1.15; margin-top: 0.2rem; font-variant-numeric: tabular-nums;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.kpi-valor.texto { font-size: 1.15rem; padding-top: 0.25rem; }
.kpi-nota { font-size: 0.78rem; color: #64748B; margin-top: 0.1rem; }
.kpi.destacado { border-left: 4px solid #0B3C8C; }

/* Paneles del mapa y del ranking */
.st-key-geo_mapa, .st-key-geo_ranking {
    background: #FFFFFF;
    border: 1px solid #E3E8F0;
    border-radius: 12px;
    padding: 0.8rem 1rem 0.4rem 1rem !important;
}
.st-key-geo_tabla {
    background: #FFFFFF;
    border: 1px solid #E3E8F0;
    border-radius: 12px;
    padding: 0.9rem 1.1rem 0.9rem 1.1rem !important;
}
.resumen { margin: 0.6rem 0 0.9rem 0; border-top: 1px solid #EEF2F7; }
.resumen div {
    display: flex; justify-content: space-between; gap: 1rem;
    padding: 0.5rem 0; border-bottom: 1px solid #EEF2F7; font-size: 0.85rem;
}
.resumen span { color: #64748B; }
.resumen b { color: #0F2744; font-weight: 600; text-align: right; }
.panel-titulo { font-family: 'Poppins', sans-serif; font-size: 0.95rem; font-weight: 700; color: #0F2744; }
.panel-sub { font-size: 0.78rem; color: #94A3B8; margin-top: -0.1rem; }

@media (max-width: 900px) {
    .kpis { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
</style>
"""


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

    datos = pd.read_csv(DATOS, dtype={"cod_mun": str, "evento": str})

    poblacion = None
    if os.path.exists(POBLACION):
        poblacion = pd.read_csv(POBLACION, dtype={"cod_mun": str})

    return geo, base, datos, poblacion


def _kpi(label, valor, nota="", clase="", texto=False):
    return (
        f'<div class="kpi {clase}">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-valor{" texto" if texto else ""}">{valor}</div>'
        f'<div class="kpi-nota">{nota}</div>'
        '</div>'
    )


def render_mapa():
    st.markdown(ESTILOS, unsafe_allow_html=True)

    geo, base, datos, poblacion = cargar_datos(os.path.getmtime(DATOS))
    total_municipios = len(base)

    # ------------------------------------------------------------------
    # Barra de filtros (una sola fila)
    # ------------------------------------------------------------------
    with st.container(key="geo_filtros"):
        columnas = [3.2, 1, 2.6, 2.2] + ([1.8] if poblacion is not None else [])
        cols = st.columns(columnas, vertical_alignment="bottom")

        eventos = sorted(datos["evento"].unique())
        evento = cols[0].selectbox(
            "Evento de interés en salud pública",
            eventos,
            format_func=lambda e: NOMBRES_EVENTO.get(e, e),
        )

        anios = sorted(datos["anio"].unique(), reverse=True)
        anio = cols[1].selectbox("Año", anios)

        sub = datos[(datos["evento"] == evento) & (datos["anio"] == anio)].copy()
        if sub.empty:
            st.warning("No hay registros para el evento y año seleccionados.")
            return

        sem_min, sem_max = int(sub["semana"].min()), int(sub["semana"].max())
        if sem_min == sem_max:
            sem_ini = sem_fin = sem_min
            cols[2].text_input("Semana epidemiológica", f"SE {sem_min}", disabled=True)
        else:
            sem_ini, sem_fin = cols[2].slider(
                "Semana epidemiológica",
                min_value=sem_min,
                max_value=sem_max,
                value=(sem_min, sem_max),
            )

        municipios = ["Todos los municipios"] + sorted(base["municipio"].dropna().unique().tolist())
        municipio_sel = cols[3].selectbox("Municipio", municipios)

        indicador = "Casos"
        if poblacion is not None:
            indicador = cols[4].selectbox("Indicador", ["Casos", "Tasa x 100.000 hab."])

    sub = sub[(sub["semana"] >= sem_ini) & (sub["semana"] <= sem_fin)]

    # ------------------------------------------------------------------
    # Agregación por municipio
    # ------------------------------------------------------------------
    agg = sub.groupby("cod_mun", as_index=False)["casos"].sum()
    df = base.merge(agg, on="cod_mun", how="left")
    df["casos"] = df["casos"].fillna(0).astype(int)

    es_tasa = indicador.startswith("Tasa")
    if es_tasa:
        df = df.merge(poblacion[["cod_mun", "poblacion"]], on="cod_mun", how="left")
        df["valor"] = (df["casos"] / df["poblacion"] * 100000).round(1)
        etiqueta = "Tasa x 100.000"
    else:
        df["valor"] = df["casos"]
        etiqueta = "Casos"

    total_dpto = int(df["casos"].sum())
    con_casos = int((df["casos"] > 0).sum())
    top = df.sort_values("casos", ascending=False).iloc[0]
    rango_se = f"SE {sem_ini}" if sem_ini == sem_fin else f"SE {sem_ini} a {sem_fin}"

    # ------------------------------------------------------------------
    # Indicadores
    # ------------------------------------------------------------------
    if municipio_sel == "Todos los municipios":
        k1 = _kpi("Casos en el departamento", f"{total_dpto:,}".replace(",", "."), f"{rango_se} · {anio}", "destacado")
    else:
        casos_mun = int(df.loc[df["municipio"] == municipio_sel, "casos"].sum())
        part = f"{casos_mun / total_dpto * 100:.1f}% del departamento" if total_dpto else "Sin casos en el departamento"
        k1 = _kpi(f"Casos en {municipio_sel}", f"{casos_mun:,}".replace(",", "."), part, "destacado")

    k2 = _kpi("Municipios con casos", f"{con_casos}<small style='font-size:0.95rem;color:#94A3B8;font-weight:600;'> / {total_municipios}</small>",
              f"{con_casos / total_municipios * 100:.0f}% del territorio")
    if total_dpto:
        k3 = _kpi("Mayor número de casos", top["municipio"], f"{int(top['casos'])} casos · {top['casos'] / total_dpto * 100:.0f}% del total", texto=True)
    else:
        k3 = _kpi("Mayor número de casos", "—", "Sin casos en el periodo", texto=True)
    semanas = sem_fin - sem_ini + 1
    k4 = _kpi("Promedio semanal", f"{total_dpto / semanas:.1f}".replace(".", ","), f"casos por semana · {semanas} SE")

    st.markdown(f'<div class="kpis">{k1}{k2}{k3}{k4}</div>', unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # Mapa + ranking
    # ------------------------------------------------------------------
    nombre_evento = NOMBRES_EVENTO.get(evento, evento)
    alto = 500
    c_mapa, c_rank = st.columns([1.55, 1], gap="small")

    with c_mapa:
        with st.container(key="geo_mapa"):
            st.markdown(
                f'<div class="panel-titulo">Distribución por municipio</div>'
                f'<div class="panel-sub">{nombre_evento} · {rango_se} · {anio}</div>',
                unsafe_allow_html=True,
            )

            df_mapa = df.copy()
            df_mapa["resaltado"] = (
                df_mapa["municipio"] == municipio_sel
                if municipio_sel != "Todos los municipios" else False
            )
            maximo = max(float(df_mapa["valor"].max() or 0), 1.0)

            fig = px.choropleth(
                df_mapa,
                geojson=geo,
                locations="cod_mun",
                featureidkey="properties.cod_mun",
                color="valor",
                color_continuous_scale=ESCALA,
                range_color=(0, maximo),
                custom_data=["municipio", "casos", "valor"],
            )
            fig.update_geos(fitbounds="locations", visible=False, bgcolor="rgba(0,0,0,0)")
            fig.update_traces(
                marker_line_color=[AZUL if r else "#FFFFFF" for r in df_mapa["resaltado"]],
                marker_line_width=[3 if r else 0.9 for r in df_mapa["resaltado"]],
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>Casos: %{customdata[1]}"
                    + ("<br>Tasa x 100.000: %{customdata[2]}" if es_tasa else "")
                    + "<extra></extra>"
                ),
            )
            fig.update_layout(
                height=alto,
                margin={"r": 0, "t": 4, "l": 0, "b": 0},
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", color="#334155"),
                hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#CBD5E1", font_size=12),
                coloraxis_colorbar=dict(
                    title=dict(text=etiqueta, font=dict(size=11)),
                    thickness=10,
                    len=0.55,
                    x=0.98,
                    xanchor="right",
                    y=0.5,
                    tickfont=dict(size=10),
                    outlinewidth=0,
                ),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c_rank:
        with st.container(key="geo_ranking"):
            st.markdown(
                '<div class="panel-titulo">Municipios con más casos</div>'
                f'<div class="panel-sub">{etiqueta} · ordenados de mayor a menor</div>',
                unsafe_allow_html=True,
            )
            rank = df[df["casos"] > 0].sort_values("valor", ascending=True)
            if rank.empty:
                st.info("No se registraron casos en el periodo seleccionado.")
            else:
                colores = [
                    AZUL if (municipio_sel == "Todos los municipios" or m == municipio_sel) else "#C7D3E6"
                    for m in rank["municipio"]
                ]
                barras = px.bar(rank, x="valor", y="municipio", orientation="h", text="valor")
                barras.update_traces(
                    marker_color=colores,
                    texttemplate="%{text}",
                    textposition="outside",
                    textfont=dict(size=11, color="#334155"),
                    cliponaxis=False,
                    hovertemplate="<b>%{y}</b><br>" + etiqueta + ": %{x}<extra></extra>",
                )
                barras.update_layout(
                    height=alto,
                    margin={"r": 30, "t": 4, "l": 0, "b": 0},
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter, sans-serif", size=12, color="#334155"),
                    xaxis=dict(visible=False),
                    yaxis=dict(title=None, tickfont=dict(size=12)),
                    bargap=0.35,
                    showlegend=False,
                )
                st.plotly_chart(barras, use_container_width=True, config={"displayModeBar": False})

    # ------------------------------------------------------------------
    # Tabla de casos (compacta) y descarga
    # ------------------------------------------------------------------
    tabla = df.sort_values(["valor", "municipio"], ascending=[False, True]).copy()
    tabla["pct"] = (tabla["casos"] / total_dpto * 100).round(1) if total_dpto else 0.0
    cols_tabla = ["municipio", "casos", "pct"] + (["valor"] if es_tasa else [])
    tabla = tabla[cols_tabla]

    with st.container(key="geo_tabla"):
        t1, t2 = st.columns([1.55, 1], gap="large", vertical_alignment="top")
        with t1:
            st.markdown(
                '<div class="panel-titulo">Tabla de casos por municipio</div>'
                f'<div class="panel-sub">{nombre_evento} · {rango_se} · {anio}</div>',
                unsafe_allow_html=True,
            )
            config_cols = {
                "municipio": st.column_config.TextColumn("Municipio", width="medium"),
                "casos": st.column_config.ProgressColumn(
                    "Casos", format="%d", min_value=0, max_value=max(int(tabla["casos"].max()), 1), width="medium"
                ),
                "pct": st.column_config.NumberColumn("% del total", format="%.1f %%", width="small"),
            }
            if es_tasa:
                config_cols["valor"] = st.column_config.NumberColumn("Tasa x 100.000", format="%.1f", width="small")
            st.dataframe(
                tabla,
                hide_index=True,
                use_container_width=True,
                height=36 * (len(tabla) + 1) + 3,
                column_config=config_cols,
            )
        with t2:
            st.markdown(
                '<div class="panel-titulo">Resumen del periodo</div>'
                '<div class="resumen">'
                f'<div><span>Evento</span><b>{nombre_evento}</b></div>'
                f'<div><span>Periodo</span><b>{rango_se} · {anio}</b></div>'
                f'<div><span>Total de casos</span><b>{total_dpto}</b></div>'
                f'<div><span>Municipios con casos</span><b>{con_casos} de {total_municipios}</b></div>'
                f'<div><span>Municipios sin casos</span><b>{total_municipios - con_casos}</b></div>'
                '</div>',
                unsafe_allow_html=True,
            )
            st.download_button(
                "Descargar tabla (CSV)",
                tabla.rename(columns={"municipio": "Municipio", "casos": "Casos", "pct": "% del total", "valor": etiqueta})
                .to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig"),
                file_name=f"casos_{evento}_{anio}_SE{sem_ini}-{sem_fin}.csv",
                mime="text/csv",
                icon=":material/download:",
                use_container_width=True,
            )

    nota = "Fuente: Sivigila. Casos por municipio de procedencia."
    if es_tasa:
        nota += " La tasa usa población DANE; interprétela con cautela."
    st.caption(nota)


if __name__ == "__main__":
    render_mapa()
