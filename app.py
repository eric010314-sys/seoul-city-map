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
    initial_sidebar_state="collapsed",
)

st.markdown("""
    <style>
    /* 전체 여백 제거 */
    .block-container {
        padding: 0.4rem 0.6rem 0rem !important;
        max-width: 100% !important;
    }
    /* 상단 헤더 영역 숨김 */
    header[data-testid="stHeader"] { display: none; }
    /* 사이드바 토글 버튼 위치 조정 */
    [data-testid="collapsedControl"] { top: 0.3rem; }
    /* 제목 크기 */
    h1 { font-size: 1rem !important; margin: 0 0 0.3rem 0 !important; }
    /* metric 카드 크기 */
    [data-testid="stMetric"] {
        background: #1e293b;
        border-radius: 8px;
        padding: 0.4rem 0.5rem !important;
    }
    [data-testid="stMetricLabel"] { font-size: 0.65rem !important; }
    [data-testid="stMetricValue"] { font-size: 0.95rem !important; }
    [data-testid="stMetricDelta"] { font-size: 0.65rem !important; }
    /* 탭 크기 */
    .stTabs [data-baseweb="tab"] { font-size: 0.75rem; padding: 0.3rem 0.6rem; }
    /* 캡션 */
    .stCaption { font-size: 0.65rem !important; }
    /* 컬럼 간격 */
    [data-testid="column"] { padding: 0 0.15rem !important; }
    </style>
""", unsafe_allow_html=True)


def main():
    filters = render_sidebar()

    st.title("서울 실시간 도시 현황")

    with st.spinner("불러오는 중..."):
        noise_df = fetch_noise_data()
        pop_df   = fetch_population_data()
        green_df = fetch_green_data()

    render_kpi_row(filters["overlay"], noise_df, pop_df, green_df)

    m = build_map(
        noise_df, pop_df, green_df,
        overlay=filters["overlay"],
        selected_district=filters["selected_district"],
    )
    st.pydeck_chart(m, width="stretch", height=320)

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
