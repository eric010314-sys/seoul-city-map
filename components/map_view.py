import pydeck as pdk
import pandas as pd
import requests
import streamlit as st

SEOUL_GEOJSON_URL = (
    "https://raw.githubusercontent.com/southkorea/seoul-maps/master/"
    "kostat/2013/json/seoul_municipalities_geo_simple.json"
)

# 색상 구간: (정규화값, [R,G,B,A])
_COLORS = {
    "녹지율":  [(0.0, [180,120,60,210]), (0.5, [100,180,50,210]), (1.0, [30,100,30,220])],
    "유동인구": [(0.0, [219,234,254,200]), (0.5, [59,130,246,215]), (1.0, [30,64,175,230])],
    "소음":    [(0.0, [46,204,113,210]), (0.4, [241,196,30,210]), (0.7, [230,126,34,215]), (1.0, [231,76,60,220])],
}


@st.cache_data(ttl=3600, show_spinner=False)
def load_geojson() -> dict:
    resp = requests.get(SEOUL_GEOJSON_URL, timeout=10)
    resp.raise_for_status()
    return resp.json()


def build_map(
    noise_df: pd.DataFrame,
    pop_df: pd.DataFrame,
    green_df: pd.DataFrame,
    overlay: str = "녹지율",
    selected_district: str = "전체",
) -> pdk.Deck:
    geo = load_geojson()

    # 오버레이별 데이터 컬럼 및 설정
    cfg = {
        "녹지율":  {"df": green_df,  "col": "green_ratio", "unit": "%",  "label": "녹지율"},
        "유동인구": {"df": pop_df,    "col": "population",  "unit": "명",  "label": "추정인구"},
        "소음":    {"df": noise_df,  "col": "noise_db",    "unit": "dB",  "label": "소음도"},
    }[overlay]

    col    = cfg["col"]
    unit   = cfg["unit"]
    df     = cfg["df"]
    colors = _COLORS[overlay]

    val_min = df[col].min()
    val_max = df[col].max()

    # 전체 데이터 병합 (툴팁용)
    merged = green_df[["district", "green_ratio"]].merge(
        noise_df[["district", "noise_db"]],  on="district", how="outer"
    ).merge(
        pop_df[["district", "population", "congestion"]], on="district", how="outer"
    )

    rows = []
    for feat in geo["features"]:
        name = feat["properties"]["name"]
        poly = _polygon_coords(feat)
        if poly is None:
            continue

        row  = merged[merged["district"] == name]
        val  = float(row[col].iloc[0]) if not row.empty and pd.notna(row[col].iloc[0]) else None
        t    = (val - val_min) / (val_max - val_min) if val is not None and val_max > val_min else 0.0
        elev = t * 8_000

        noise_val = float(row["noise_db"].iloc[0])   if not row.empty and pd.notna(row["noise_db"].iloc[0])   else None
        pop_val   = int(row["population"].iloc[0])    if not row.empty and pd.notna(row["population"].iloc[0]) else None
        green_ratio = float(row["green_ratio"].iloc[0]) if not row.empty and pd.notna(row["green_ratio"].iloc[0]) else None
        cong      = row["congestion"].iloc[0]         if not row.empty and pd.notna(row.get("congestion", pd.Series([None])).iloc[0]) else "-"

        rows.append({
            "polygon":     poly,
            "district":    name,
            "elevation":   elev,
            "color":       [245,158,11,230] if selected_district == name else _interp(colors, t),
            "noise_str":   f"{noise_val:.1f} dB" if noise_val is not None else "-",
            "pop_str":     f"{pop_val:,} 명"      if pop_val   is not None else "-",
            "green_str":   f"{green_ratio:.2f}%" if green_ratio is not None else "-",
            "cong":        cong,
        })

    layer = pdk.Layer(
        "PolygonLayer",
        data=rows,
        get_polygon="polygon",
        get_elevation="elevation",
        get_fill_color="color",
        get_line_color=[255, 255, 255, 80],
        line_width_min_pixels=1,
        extruded=True,
        pickable=True,
        auto_highlight=True,
        highlight_color=[255, 255, 255, 60],
        elevation_scale=1,
    )

    view = pdk.ViewState(
        latitude=37.5550,
        longitude=126.9780,
        zoom=8.8,
        pitch=35,
        bearing=0,
    )

    tooltip = {
        "html": """
            <div style="font-family:sans-serif;padding:8px 12px;font-size:13px;
                        background:#1e293b;color:#f1f5f9;border-radius:8px;
                        box-shadow:0 2px 10px rgba(0,0,0,0.5);min-width:160px">
              <b style="font-size:15px;color:#f8fafc">{district}</b><br>
              <span style="color:#86efac">🌿 녹지율</span>&nbsp; {green_str}<br>
              <span style="color:#60a5fa">👥 추정인구</span>&nbsp; {pop_str}<br>
              <span style="color:#fca5a5">🔊 소음도</span>&nbsp; {noise_str}<br>
              <span style="color:#94a3b8; font-size:11px">혼잡도: {cong}</span>
            </div>
        """,
        "style": {"background": "transparent", "border": "none"},
    }

    return pdk.Deck(
        layers=[layer],
        initial_view_state=view,
        map_style="https://basemaps.cartocdn.com/gl/positron-nolabels-gl-style/style.json",
        tooltip=tooltip,
    )


def _polygon_coords(feature: dict):
    try:
        geom = feature["geometry"]
        if geom["type"] == "Polygon":
            return geom["coordinates"][0]
        return max(geom["coordinates"], key=lambda p: len(p[0]))[0]
    except Exception:
        return None


def _interp(stops: list, t: float) -> list[int]:
    t = max(0.0, min(1.0, t))
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        if t0 <= t <= t1:
            r = (t - t0) / (t1 - t0) if t1 > t0 else 0
            return [int(c0[j] + (c1[j] - c0[j]) * r) for j in range(4)]
    return list(stops[-1][1])
