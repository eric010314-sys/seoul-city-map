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
    /* 다크모드 무시, 라이트 고정 */
    html { color-scheme: light only !important; }
    .block-container {
        padding: 0.5rem 0.5rem 0rem !important;
        max-width: 100% !important;
        position: relative !important;
    }
    header[data-testid="stHeader"] { display: none; }
    [data-testid="collapsedControl"] { display: none; }
    footer { visibility: hidden !important; }
    #MainMenu { display: none; }
    [data-testid="stStatusWidget"] { display: none; }
    [data-testid="stDeckGlJsonChart"] > div { border: none !important; border-radius: 0 !important; }
    [data-testid="stDeckGlJsonChart"] iframe { border: none !important; }
    [data-testid="StyledFullScreenButton"],
    button[title="View fullscreen"],
    button[aria-label="Fullscreen"],
    .stDeckGlJsonChart ~ div button { display: none !important; }

    /* 세그먼트 토글 스타일 */
    [data-testid="stSegmentedControl"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        position: absolute !important;
        top: 1rem !important;
        left: 1rem !important;
        z-index: 10 !important;
    }
    [data-testid="stSegmentedControl"] button {
        background: #E5EBDB !important;
        color: #476844 !important;
        border-radius: 999px !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        padding: 0.35rem 1rem !important;
        border: none !important;
    }
    [data-testid="stSegmentedControl"] button[aria-pressed="true"],
    [data-testid="stSegmentedControl"] button:hover,
    [data-testid="stSegmentedControl"] button:focus {
        background: #E5EBDB !important;
        color: #476844 !important;
        border: none !important;
        box-shadow: none !important;
    }
    [data-testid="stSegmentedControl"] button * {
        color: #476844 !important;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    with st.spinner("불러오는 중..."):
        noise_df = fetch_noise_data()
        pop_df   = fetch_population_data()
        green_df = fetch_green_data()

    overlay_label = st.segmented_control(
        label="",
        options=["🌿 녹지율(%)", "👥 유동인구", "🔊 소음"],
        default="🌿 녹지율(%)",
        label_visibility="collapsed",
    )

    overlay_key = {
        "🌿 녹지율(%)": "녹지율",
        "👥 유동인구": "유동인구",
        "🔊 소음": "소음",
    }.get(overlay_label, "녹지율")

    m = build_map(noise_df, pop_df, green_df, overlay=overlay_key)
    st.pydeck_chart(m, width="stretch", height=480)


if __name__ == "__main__":
    main()
