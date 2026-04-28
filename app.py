import time
import streamlit as st

from api.noise import fetch_noise_data
from api.population import fetch_population_data
from api.green_space import fetch_green_data
from components.sidebar import render_sidebar
from components.map_view import build_map
from components.metrics import render_kpi_row, render_district_detail, render_ranking_table
from config import REFRESH_INTERVAL

st.set_page_config(
    page_title="서울 실시간 도시 현황",
    page_icon="🗺️",
    layout="wide",
)

def main():
    filters = render_sidebar()

    st.title("서울 실시간 도시 현황 대시보드")
    st.caption(f"유동인구·소음 데이터는 {REFRESH_INTERVAL // 60}분마다 갱신 / 녹지율은 정적 데이터")

    with st.spinner("데이터 불러오는 중..."):
        noise_df = fetch_noise_data()
        pop_df   = fetch_population_data()
        green_df = fetch_green_data()

    render_kpi_row(filters["overlay"], noise_df, pop_df, green_df)

    m = build_map(
        noise_df, pop_df, green_df,
        overlay=filters["overlay"],
        selected_district=filters["selected_district"],
    )
    st.pydeck_chart(m, width="stretch", height=640)

    tab1, tab2 = st.tabs(["자치구 상세", "전체 랭킹"])
    with tab1:
        render_district_detail(filters["selected_district"], noise_df, pop_df, green_df)
    with tab2:
        render_ranking_table(noise_df, pop_df, green_df, filters["overlay"])

    if filters["auto_refresh"]:
        time.sleep(REFRESH_INTERVAL)
        st.cache_data.clear()
        st.rerun()


if __name__ == "__main__":
    main()
