import pandas as pd
from pathlib import Path

GREEN_CSV = Path(__file__).parent.parent / "자치구별 녹지통계.csv"


def fetch_green_data() -> pd.DataFrame:
    """
    자치구별 녹지통계 CSV 로드.
    컬럼: district (str), green_area (float, ㎡)
    """
    df = pd.read_csv(GREEN_CSV, encoding="utf-8-sig")
    df = df[["자치구", "합계_면적(㎡)"]].rename(columns={
        "자치구":       "district",
        "합계_면적(㎡)": "green_area",
    })
    df["green_area"] = pd.to_numeric(df["green_area"], errors="coerce")
    return df
