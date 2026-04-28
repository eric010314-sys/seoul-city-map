import streamlit as st

from api.noise import fetch_noise_data
from api.population import fetch_population_data
from api.green_space import fetch_green_data
from components.map_view import build_map

st.set_page_config(
    page_title="서울 실시간 도시 현황",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
    <style>
    .block-container { padding: 0.5rem 0.5rem 0rem !important; max-width: 100% !important; }
    header[data-testid="stHeader"] { display: none; }
    [data-testid="collapsedControl"] { display: none; }
    div[role="radiogroup"] { gap: 0.4rem; }
    div[role="radiogroup"] label {
        background: #1e293b;
        border-radius: 20px;
        padding: 0.3rem 1rem !important;
        font-size: 0.85rem !important;
        border: 1px solid #334155;
    }
    div[role="radiogroup"] label:has(input:checked) {
        background: #3b82f6 !important;
        border-color: #3b82f6 !important;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    with st.spinner("불러오는 중..."):
        noise_df = fetch_noise_data()
        pop_df   = fetch_population_data()
        green_df = fetch_green_data()

    overlay = st.radio(
        label="",
        options=["🌿 녹지율", "👥 유동인구", "🔊 소음"],
        horizontal=True,
        label_visibility="collapsed",
    )

    overlay_key = {"🌿 녹지율": "녹지율", "👥 유동인구": "유동인구", "🔊 소음": "소음"}[overlay]

    m = build_map(noise_df, pop_df, green_df, overlay=overlay_key)
    st.pydeck_chart(m, width="stretch", height=620)


if __name__ == "__main__":
    main()
