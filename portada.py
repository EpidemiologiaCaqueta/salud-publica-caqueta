"""Portada del portal: cifras y gráficos calculados de los tableros ya publicados
(tablero_eisp.html, tablero_geo.html, tablero_tb.html y tablero_estadisticas_vitales.html).
No lee bases con datos personales: solo los cubos agregados que traen esos HTML."""
import base64
import html as _h
import json
import os
import re
from pathlib import Path

import streamlit as st

CARPETA = Path(__file__).parent
ARCHIVOS = ["tablero_eisp.html", "tablero_geo.html", "tablero_tb.html", "tablero_estadisticas_vitales.html"]
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def version():
    return tuple(os.path.getmtime(CARPETA / f) if (CARPETA / f).exists() else 0 for f in ARCHIVOS)


def _json(texto, clave):
    i = texto.index('{"' + clave + '"')
    return json.JSONDecoder().raw_decode(texto[i:])[0]


def _total(cubo, filtro=None):
    return sum(r[-1] for r in cubo["rows"] if filtro is None or filtro(r))


def _agrupa(cubo, dim, filtro=None):
    k = cubo["dims"].index(dim)
    out = {}
    for r in cubo["rows"]:
        if filtro is None or filtro(r):
            v = cubo["dic"][dim][r[k]]
            out[v] = out.get(v, 0) + r[-1]
    return out


def _fmt(n):
    return f"{n:,.0f}".replace(",", ".")


@st.cache_data(show_spinner=False)
def resumen(_version=None):
    r = {}
    try:
        e = _json((CARPETA / "tablero_eisp.html").read_text(encoding="utf-8"), "eisp")
        c = e["eisp"]
        aj = c["dims"].index("Ajuste")
        desc = c["dic"]["Ajuste"].index("Descartado") if "Descartado" in c["dic"]["Ajuste"] else -1
        ok = lambda row: row[aj] != desc
        sem = _agrupa(c, "Semana", ok)
        ev = _agrupa(c, "Evento", ok)
        mun = _agrupa(c, "Mpio procedencia", ok)
        cf = _agrupa(c, "Condición final", ok)
        g = e["generado"][:10].split("-")
        r.update(
            anio=e["anio"], semana=e["se"], se_fechas=e["se_fechas"],
            generado=f"{int(g[2])} {MESES[int(g[1]) - 1]} {g[0]}",
            casos=_total(c, ok), eventos=len(ev),
            semanas=[sem.get(str(s).zfill(2), 0) for s in range(1, e["se"] + 1)],
            top=sorted(ev.items(), key=lambda x: -x[1]),
            municipios=mun, mapa=e["mapa"], poblacion=e.get("poblacion", {}), fallecidos=cf.get("Fallecido", 0),
        )
    except Exception:
        return None
    try:
        g = (CARPETA / "tablero_geo.html").read_text(encoding="utf-8")
        r["ubicados"] = int(re.search(r'"ubicados":(\d+)', g).group(1))
    except Exception:
        r["ubicados"] = None
    try:
        t = _json((CARPETA / "tablero_tb.html").read_text(encoding="utf-8"), "tb")["tb"]
        aj = t["dims"].index("Ajuste")
        desc = t["dic"]["Ajuste"].index("Descartado") if "Descartado" in t["dic"]["Ajuste"] else -1
        r["tb"] = _total(t, lambda row: row[aj] != desc)
    except Exception:
        r["tb"] = None
    try:
        v = _json((CARPETA / "tablero_estadisticas_vitales.html").read_text(encoding="utf-8"), "nac")
        anio = str(r["anio"])
        for k in ("nac", "def"):
            cub = v[k]
            ia = cub["dims"].index("Año")
            ix = cub["dic"]["Año"].index(anio) if anio in cub["dic"]["Año"] else -1
            r[k] = _total(cub, lambda row: row[ia] == ix)
        r["corte_vit"] = v["corte"].split(", ", 1)[-1]
    except Exception:
        r["nac"] = r["def"] = None
    return r


def b64(nombre):
    p = CARPETA / nombre
    return base64.b64encode(p.read_bytes()).decode() if p.exists() else ""


# ------------------------------------------------------------------ iconos
_IC = {
    "pulso": '<path d="M3 12h4l3-8 4 16 3-8h4"/>',
    "pulmon": '<path d="M12 4v8"/><path d="M12 12c-1.5 1-3 1-3 1"/><path d="M12 12c1.5 1 3 1 3 1"/><path d="M8.5 7C5 7 3 11.5 3 16c0 2.5 1.6 4 3.5 4S10 19 10 17v-6"/><path d="M15.5 7C19 7 21 11.5 21 16c0 2.5-1.6 4-3.5 4S14 19 14 17v-6"/>',
    "bebe": '<circle cx="12" cy="7" r="3.2"/><path d="M5 21c0-4 3.1-7 7-7s7 3 7 7"/><path d="M10.6 6.2c.6-.7 2.2-.7 2.8 0"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.6"/>',
    "diario": '<rect x="3" y="4" width="15" height="16" rx="2"/><path d="M18 8h2a1 1 0 0 1 1 1v9a2 2 0 0 1-2 2"/><path d="M7 8h7M7 12h7M7 16h4"/>',
    "libro": '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5"/><path d="M9 7h6M9 11h6"/>',
    "casos": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "semana": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/><path d="M8 15h3"/>',
    "cruz": '<path d="M12 3v18M7 8h10"/>',
    "reloj": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "datos": '<ellipse cx="12" cy="5.5" rx="8" ry="2.8"/><path d="M4 5.5v13c0 1.5 3.6 2.8 8 2.8s8-1.3 8-2.8v-13"/><path d="M4 12c0 1.5 3.6 2.8 8 2.8s8-1.3 8-2.8"/>',
}


def icono(n, color="currentColor", tam=22):
    return (f'<svg width="{tam}" height="{tam}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{_IC[n]}</svg>')


# ------------------------------------------------------------------ piezas HTML
def _nombre_evento(ev):
    cod, _, nom = ev.partition(" - ")
    nom = nom.strip().capitalize()
    for a, b in (("vih", "VIH"), ("sida", "SIDA"), ("ira", "IRA"), ("esavi", "ESAVI"), ("covid", "COVID")):
        nom = re.sub(rf"\b{a}\b", b, nom, flags=re.I)
    return cod.strip(), nom


def mapa(r):
    m, mun, pob = r["mapa"], r["municipios"], r.get("poblacion", {})
    tasa = {k: 1e5 * mun.get(k, 0) / pob[k] for k in m["mpios"] if pob.get(k)}
    orden = sorted(tasa.values())
    cortes = [orden[int(len(orden) * q / 5)] for q in range(1, 5)] if orden else []
    cols = ["#2E5FAE", "#5585CC", "#86AADF", "#BCD2F0", "#FFFFFF"]
    partes = []
    for nombre, p in m["mpios"].items():
        t = tasa.get(nombre)
        c = cols[sum(t >= x for x in cortes)] if t is not None else "#2E5FAE"
        partes.append(f'<path d="{p["d"]}" fill="{c}" stroke="#0B3C8C" stroke-width="1.2">'
                      f'<title>{_h.escape(nombre.title())}: {_fmt(mun.get(nombre, 0))} casos · '
                      f'{(f"{t:,.0f}".replace(",", ".") if t is not None else "–")} por 100 mil hab.</title></path>')
    top = max(tasa, key=tasa.get) if tasa else ""
    ley = "".join(f'<i style="background:{c}"></i>' for c in cols)
    return (f'<svg class="h-mapa" viewBox="-6 -6 {m["w"] + 12} {m["h"] + 12}" preserveAspectRatio="xMidYMid meet">'
            f'<g filter="url(#sombra)">{"".join(partes)}</g>'
            '<defs><filter id="sombra" x="-10%" y="-10%" width="120%" height="120%">'
            '<feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#020b24" flood-opacity=".45"/></filter></defs></svg>'
            f'<div class="h-mapa-ley"><span>Menor</span><span class="ley-q">{ley}</span><span>Mayor tasa</span></div>'
            f'<div class="h-mapa-nota">Tasa más alta: <b>{_h.escape(top.title())}</b> · {_fmt(tasa.get(top, 0))} casos por 100 mil hab. '
            f'· Florencia concentra {_fmt(mun.get("FLORENCIA", 0))} casos</div>')


def hero(r, logos):
    chips = (f'<span class="h-chip"><span class="punto"></span>Datos a la SE {r["semana"]} de {r["anio"]} · {r["se_fechas"]}</span>'
             f'<span class="h-chip">{icono("reloj", "#BFD3F3", 15)} Actualizado {r["generado"]}</span>'
             f'<span class="h-chip">{icono("datos", "#BFD3F3", 15)} Sivigila · RUAF-ND · DANE</span>')
    logos_html = "".join(f'<img src="data:image/png;base64,{b}" alt="">' for b in logos if b)
    return (
        '<div class="h2o">'
        '<div class="h-izq">'
        f'<div class="h-logos">{logos_html}</div>'
        '<p class="h-eyebrow">Secretaría de Salud Departamental del Caquetá</p>'
        '<h1 class="h-titulo">Portal de Vigilancia<br>Epidemiológica</h1>'
        '<p class="h-sub">Cifras oficiales y tableros interactivos de los eventos de interés en salud pública '
        'notificados al Sivigila, tuberculosis, estadísticas vitales y georreferenciación de casos en los 16 municipios.</p>'
        f'<div class="h-chips">{chips}</div>'
        '</div>'
        f'<div class="h-der"><div class="h-mapa-tit">Tasa de notificación por municipio de procedencia · {r["anio"]}</div>{mapa(r)}</div>'
        '</div>'
    )


def kpis(r):
    sem = r["semanas"]
    u4 = sum(sem[-4:])
    var = f'SE {max(r["semana"] - 3, 1)} a {r["semana"]} · promedio del año: {_fmt(4 * sum(sem) / len(sem))}' if sem else ""
    pg = f'{100 * r["ubicados"] / r["casos"]:.0f}% de los casos con ubicación' if r.get("ubicados") else "Mapa de focos y calor"
    items = [
        ("casos", "#0B3C8C", "#E8EFFB", _fmt(r["casos"]), "Casos notificados EISP", f'{r["eventos"]} eventos de interés · {r["anio"]}'),
        ("semana", "#0F8F86", "#E3F5F3", _fmt(u4), "Casos últimas 4 semanas", var),
        ("pin", "#6B4F9E", "#EFEAF7", _fmt(r["ubicados"]) if r.get("ubicados") is not None else "–", "Casos georreferenciados", pg),
        ("pulmon", "#BE123C", "#FCE8EC", _fmt(r["tb"]) if r.get("tb") is not None else "–", "Casos de tuberculosis", "Evento 813 · casos activos"),
        ("bebe", "#1F63C6", "#E6F0FC", _fmt(r["nac"]) if r.get("nac") is not None else "–", f'Nacimientos {r["anio"]}', f'RUAF-ND · corte {r.get("corte_vit", "")}'),
        ("cruz", "#475569", "#EEF1F5", _fmt(r["def"]) if r.get("def") is not None else "–", f'Defunciones {r["anio"]}', f'RUAF-ND · corte {r.get("corte_vit", "")}'),
    ]
    return '<div class="kpis">' + "".join(
        f'<div class="kpi"><div class="k-ic" style="background:{bg}">{icono(ic, col)}</div>'
        f'<div class="k-tx"><div class="k-val" style="color:{col}">{val}</div><div class="k-lab">{lab}</div>'
        f'<div class="k-sub">{sub}</div></div></div>'
        for ic, col, bg, val, lab, sub in items) + '</div>'


def curva(r):
    s = r["semanas"]
    W, H, pl, pb, pt = 760, 210, 30, 22, 14
    mx = max(s) if s else 1
    paso = 10 ** len(str(int(mx))) / 10
    tope = -(-mx // paso) * paso if mx else 1
    if tope / paso > 6:
        paso *= 2
        tope = -(-mx // paso) * paso
    bw = (W - pl) / max(len(s), 1)
    prom = sum(s) / len(s) if s else 0
    y = lambda v: pt + (H - pt - pb) * (1 - v / tope)
    g = []
    v = 0
    while v <= tope:
        g.append(f'<line x1="{pl}" x2="{W}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="#E8EDF4"/>'
                 f'<text x="{pl - 6}" y="{y(v) + 3.5:.1f}" text-anchor="end" class="ax">{_fmt(v)}</text>')
        v += paso
    for i, n in enumerate(s):
        x = pl + i * bw + 1
        ultima = i == len(s) - 1
        g.append(f'<rect x="{x:.1f}" y="{y(n):.1f}" width="{max(bw - 2, 1):.1f}" height="{max(y(0) - y(n), 0):.1f}" rx="2" '
                 f'fill="{"#F59E0B" if ultima else "#1F63C6"}"><title>SE {i + 1}: {_fmt(n)} casos</title></rect>')
        if (i + 1) % 5 == 0 or i == 0 or ultima:
            g.append(f'<text x="{x + bw / 2 - 1:.1f}" y="{H - 6}" text-anchor="middle" class="ax">{i + 1}</text>')
    g.append(f'<line x1="{pl}" x2="{W}" y1="{y(prom):.1f}" y2="{y(prom):.1f}" stroke="#0F2744" stroke-dasharray="4 4" stroke-width="1.2"/>'
             f'<text x="{W - 2}" y="{y(prom) - 5:.1f}" text-anchor="end" class="ax fuerte">Promedio {_fmt(prom)} por semana</text>')
    return (f'<div class="pc"><div class="pc-h">{icono("casos", "#0B3C8C", 18)}<span>Notificación semanal de eventos de interés · {r["anio"]}</span>'
            f'<em><i style="background:#1F63C6"></i>Casos <i style="background:#F59E0B"></i>SE {r["semana"]} en consolidación</em></div>'
            f'<svg viewBox="0 0 {W} {H}" class="pc-svg">{"".join(g)}</svg></div>')


def top_eventos(r, n=7):
    t = r["top"][:n]
    mx = t[0][1] if t else 1
    filas = []
    for ev, c in t:
        cod, nom = _nombre_evento(ev)
        filas.append(f'<div class="te" title="{_h.escape(cod + " - " + nom)}: {_fmt(c)} casos"><div class="te-n"><b>{_h.escape(cod)}</b>{_h.escape(nom)}</div>'
                     f'<div class="te-b"><i style="width:{100 * c / mx:.1f}%"></i></div>'
                     f'<div class="te-v">{_fmt(c)}<small>{100 * c / r["casos"]:.1f}%</small></div></div>')
    return (f'<div class="pc"><div class="pc-h">{icono("pulso", "#0B3C8C", 18)}<span>Eventos más notificados</span>'
            f'<em>de {r["eventos"]} eventos</em></div><div class="te-lista">{"".join(filas)}</div></div>')


CSS = """<style>
.h2o { display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); gap: 1.5rem; align-items: center;
  background: radial-gradient(120% 140% at 100% 0%, #1F63C6 0%, #0B3C8C 42%, #071F4E 100%);
  border-radius: 22px; padding: 1.2rem 1.8rem; position: relative; overflow: hidden;
  box-shadow: 0 18px 40px -18px rgba(7,31,78,.65); }
.h2o::before { content: ""; position: absolute; inset: 0; opacity: .5;
  background-image: radial-gradient(rgba(255,255,255,.09) 1px, transparent 1px); background-size: 18px 18px; }
.h-izq, .h-der { position: relative; z-index: 1; }
.h-logos { display: inline-flex; align-items: center; gap: 1.1rem; background: #FFFFFF; border-radius: 14px;
  padding: .4rem .9rem; margin-bottom: .8rem; box-shadow: 0 6px 18px rgba(2,11,36,.25); }
.h-logos img { height: 48px; width: auto; object-fit: contain; }
.h-eyebrow { color: #9CC0F5 !important; font-size: .74rem !important; font-weight: 700; letter-spacing: .16em;
  text-transform: uppercase; margin: 0 0 .45rem 0 !important; }
.h-titulo { color: #FFFFFF !important; font-family: 'Poppins', sans-serif !important; font-weight: 800 !important;
  font-size: clamp(1.6rem, 2.3vw, 2.3rem) !important; line-height: 1.08 !important; word-break: keep-all; overflow-wrap: normal; hyphens: none; margin: 0 0 .7rem 0 !important; padding: 0 !important; }
.h-sub { color: #D5E3F8 !important; font-size: .98rem !important; line-height: 1.55 !important; max-width: 640px; margin: 0 0 1rem 0 !important; }
.h-chips { display: flex; flex-wrap: wrap; gap: .5rem; }
.h-chip { display: inline-flex; align-items: center; gap: .4rem; color: #E8F0FC; font-size: .78rem; font-weight: 600;
  background: rgba(255,255,255,.1); border: 1px solid rgba(255,255,255,.18); border-radius: 999px; padding: .32rem .75rem; }
.h-chip .punto { width: 7px; height: 7px; border-radius: 50%; background: #4ADE80; box-shadow: 0 0 0 3px rgba(74,222,128,.25); }
.h-der { background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.14); border-radius: 18px; padding: .9rem 1rem .8rem; }
.h-mapa-tit { color: #BFD3F3; font-size: .74rem; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; }
.h-mapa { width: 100%; height: 190px; display: block; margin: .3rem 0; }
.h-mapa path { transition: fill .15s; } .h-mapa path:hover { fill: #FBBF24 !important; }
.h-mapa-ley { display: flex; align-items: center; gap: .5rem; color: #BFD3F3; font-size: .7rem; }
.ley-q { display: inline-flex; } .ley-q i { width: 20px; height: 8px; } .ley-q i:first-child { border-radius: 4px 0 0 4px; } .ley-q i:last-child { border-radius: 0 4px 4px 0; }
.h-mapa-nota { color: #E8F0FC; font-size: .8rem; margin-top: .35rem; }
.kpis { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: .8rem; margin: .8rem 0 0 0; }
.kpi { display: flex; gap: .75rem; align-items: flex-start; background: #FFFFFF; border: 1px solid #E3E8F0; border-radius: 16px;
  padding: .75rem .9rem; box-shadow: 0 1px 2px rgba(15,23,42,.04); }
.k-ic { flex: none; width: 42px; height: 42px; border-radius: 12px; display: grid; place-items: center; }
.k-tx { min-width: 0; }
.k-val { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 1.55rem; line-height: 1.05; font-variant-numeric: tabular-nums; }
.k-lab { color: #0F2744; font-weight: 700; font-size: .82rem; margin-top: .2rem; }
.k-sub { color: #94A3B8; font-size: .72rem; margin-top: .1rem; line-height: 1.3; }
.k-var { font-weight: 700; } .k-var.sube { color: #DC2626; } .k-var.baja { color: #16A34A; }
.graf { display: grid; grid-template-columns: minmax(0, 1.55fr) minmax(0, 1fr); gap: .8rem; margin-top: .8rem; }
.pc { background: #FFFFFF; border: 1px solid #E3E8F0; border-radius: 16px; padding: .9rem 1.1rem 1rem; }
.pc-h { display: flex; align-items: center; gap: .5rem; color: #0F2744; font-weight: 700; font-size: .92rem; margin-bottom: .4rem; }
.pc-h em { margin-left: auto; font-style: normal; font-weight: 500; color: #94A3B8; font-size: .74rem; display: flex; align-items: center; gap: .35rem; }
.pc-h em i { display: inline-block; width: 9px; height: 9px; border-radius: 3px; margin-left: .4rem; }
.pc-svg { width: 100%; height: auto; display: block; }
.pc-svg .ax { font-size: 10px; fill: #94A3B8; font-family: Inter, sans-serif; } .pc-svg .fuerte { fill: #0F2744; font-weight: 600; }
.pc-svg rect:hover { opacity: .75; }
.te-lista { display: flex; flex-direction: column; gap: .62rem; margin-top: .35rem; }
.te { display: grid; grid-template-columns: minmax(0, 1fr) 30% 74px; gap: .6rem; align-items: center; }
.te-n { font-size: .8rem; color: #334155; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.te-n b { color: #0B3C8C; font-weight: 700; margin-right: .4rem; font-variant-numeric: tabular-nums; }
.te-b { height: 9px; border-radius: 5px; background: #EEF2F8; overflow: hidden; }
.te-b i { display: block; height: 100%; border-radius: 5px; background: linear-gradient(90deg, #1F63C6, #0B3C8C); }
.te-v { text-align: right; font-weight: 700; color: #0F2744; font-size: .85rem; font-variant-numeric: tabular-nums; }
.te-v small { display: block; color: #94A3B8; font-weight: 500; font-size: .68rem; }
.tile-ic2 { width: 44px; height: 44px; border-radius: 14px; display: grid; place-items: center; }
.tile-dato { display: inline-flex; align-items: center; gap: .35rem; margin-top: .55rem; font-size: .76rem; font-weight: 600;
  border-radius: 8px; padding: .22rem .55rem; }
@media (max-width: 1250px) { .kpis { grid-template-columns: repeat(3, minmax(0, 1fr)); } .h2o { grid-template-columns: 1fr; } .h-mapa { height: 220px; } }
@media (max-width: 900px) {
  .h2o { grid-template-columns: 1fr; padding: 1.3rem 1.2rem; }
  .h-logos img { height: 36px; }
  .graf { grid-template-columns: 1fr; } .kpis { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .h-mapa { height: 190px; }
}
[class*="st-key-card_"] { padding: .85rem .95rem !important; min-height: 0 !important; gap: .25rem !important; }
[class*="st-key-card_"] .tile-title { font-size: .95rem; margin: .55rem 0 .2rem 0; }
[class*="st-key-card_"] .tile-desc { font-size: .78rem !important; line-height: 1.4 !important;
  display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
[class*="st-key-card_"] .tile-tag { font-size: .6rem; }
.block-container { padding-top: 1.1rem !important; padding-bottom: .5rem !important; }
.seccion { margin-top: .9rem !important; margin-bottom: .5rem !important; }
</style>"""
