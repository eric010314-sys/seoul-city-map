import os
from dotenv import load_dotenv

load_dotenv()

# ── API Keys (로컬: .env / 배포: Streamlit Cloud Secrets) ──
try:
    import streamlit as st
    SEOUL_API_KEY = st.secrets["SDOT_API_KEY"]
except Exception:
    SEOUL_API_KEY = os.getenv("SDOT_API_KEY", "")

# ── API Endpoints ─────────────────────────────────────────
NOISE_API_URL = "http://openapi.seoul.go.kr:8088/{key}/json/NoiseMeasure/1/25/"
POPULATION_API_URL = "http://openapi.seoul.go.kr:8088/{key}/json/citydata_ppltn/1/25/{area_name}"

# ── 서울 25개 자치구 ───────────────────────────────────────
DISTRICTS = [
    "강남구", "강동구", "강북구", "강서구", "관악구",
    "광진구", "구로구", "금천구", "노원구", "도봉구",
    "동대문구", "동작구", "마포구", "서대문구", "서초구",
    "성동구", "성북구", "송파구", "양천구", "영등포구",
    "용산구", "은평구", "종로구", "중구", "중랑구",
]

# ── 생활인구 API 지역 코드 ─────────────────────────────────
AREA_CODES = {
    "강남구": "강남 MICE 관광특구",
    "종로구": "광화문·덕수궁",
    "중구":   "명동·남대문·북창동",
    "마포구": "홍대입구역(2호선)",
}

# ── 오버레이 정의 ──────────────────────────────────────────
OVERLAYS = ["녹지율", "유동인구", "소음"]

# ── 소음 등급 기준 (dB) ────────────────────────────────────
NOISE_LEVELS = {
    "매우 조용": (0, 45),
    "보통":     (45, 55),
    "소음":     (55, 65),
    "심한 소음": (65, 200),
}

# ── 새로고침 주기 (초) ─────────────────────────────────────
REFRESH_INTERVAL = 300
