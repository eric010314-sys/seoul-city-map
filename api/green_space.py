import pandas as pd
from pathlib import Path

GREEN_CSV = Path(__file__).parent.parent / "자치구별 녹지통계.csv"

DISTRICT_AREA_KM2 = {
    "종로구": 23.91,
    "중구": 9.96,
    "용산구": 21.87,
    "성동구": 16.86,
    "광진구": 17.06,
    "동대문구": 14.22,
    "중랑구": 18.49,
    "성북구": 24.58,
    "강북구": 23.60,
    "도봉구": 20.65,
    "노원구": 35.44,
    "은평구": 29.71,
    "서대문구": 17.63,
    "마포구": 23.85,
    "양천구": 17.40,
    "강서구": 41.45,
    "구로구": 20.12,
    "금천구": 13.02,
    "영등포구": 24.55,
    "동작구": 16.35,
    "관악구": 29.57,
    "서초구": 46.98,
    "강남구": 39.50,
    "송파구": 33.88,
    "강동구": 24.59,
}


def fetch_green_data() -> pd.DataFrame:
    """
    자치구별 녹지통계 CSV 로드.
    컬럼: district, green_area, district_area, green_ratio
    """
    df = pd.read_csv(GREEN_CSV, encoding="utf-8-sig")
    df = df[["자치구", "합계_면적(㎡)"]].rename(columns={
        "자치구":       "district",
        "합계_면적(㎡)": "green_area",
    })
    df["green_area"] = pd.to_numeric(df["green_area"], errors="coerce")
    df["district_area"] = df["district"].map(DISTRICT_AREA_KM2) * 1_000_000
    df["green_ratio"] = (df["green_area"] / df["district_area"] * 100).round(2)
    return df
