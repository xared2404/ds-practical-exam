"""
Q4A Fetch multi-country panel (WB + OWID fallback)
Run:
  PYTHONPATH=src python scripts/q4a_fetch_panel_all.py

Outputs:
  data/processed/q4a_panel_country_year.parquet
"""

from __future__ import annotations
from pathlib import Path
import time
import numpy as np
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed" / "q4a_panel_country_year.parquet"
OUT.parent.mkdir(parents=True, exist_ok=True)

WB_BASE = "https://api.worldbank.org/v2"
YEARS_MIN, YEARS_MAX = 1990, 2023

WB_IND = {
    "gdp_current_usd": "NY.GDP.MKTP.CD",
    "population": "SP.POP.TOTL",
    # OJO: CO2 WB está fallando en tu sesión; lo vamos a traer de OWID
}

OWID_CO2_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"


def wb_get(url: str, params: dict, max_tries: int = 5) -> list:
    for k in range(max_tries):
        r = requests.get(url, params=params, timeout=60)
        if r.status_code == 200:
            try:
                js = r.json()
                if isinstance(js, list) and len(js) >= 2:
                    return js
            except Exception:
                pass
        time.sleep(0.8 * (2**k))
    return []


def fetch_wb_indicator_long(ind_code: str, value_name: str) -> pd.DataFrame:
    url = f"{WB_BASE}/country/all/indicator/{ind_code}"
    params = {
        "format": "json",
        "per_page": 20000,
        "date": f"{YEARS_MIN}:{YEARS_MAX}",
    }
    js = wb_get(url, params=params)
    if not js:
        print(f"[Q4A] WB failed for {ind_code} -> returning empty {value_name}")
        return pd.DataFrame(columns=["iso3", "year", value_name])

    meta, data = js[0], js[1]
    df = pd.json_normalize(data)
    if df.empty:
        return pd.DataFrame(columns=["iso3", "year", value_name])

    df = df.rename(
        columns={
            "countryiso3code": "iso3",
            "date": "year",
            "value": value_name,
        }
    )[["iso3", "year", value_name]]

    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df[value_name] = pd.to_numeric(df[value_name], errors="coerce")
    df = df.dropna(subset=["iso3", "year"]).reset_index(drop=True)

    return df


def fetch_owid_co2() -> pd.DataFrame:
    print("[Q4A] Fetching OWID CO2:", OWID_CO2_URL)
    df = pd.read_csv(OWID_CO2_URL)

    # OWID uses iso_code (ISO3) and year
    keep = ["iso_code", "year", "co2", "co2_per_capita"]
    df = df[keep].copy()
    df = df.rename(columns={"iso_code": "iso3", "co2": "co2_mt"})
    # OWID co2 is in million tonnes already (MtCO2). Keep name co2_mt for compatibility.
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["co2_mt"] = pd.to_numeric(df["co2_mt"], errors="coerce")
    df["co2_per_capita"] = pd.to_numeric(df["co2_per_capita"], errors="coerce")

    # drop aggregates/missing iso3
    df = df.dropna(subset=["iso3", "year"]).copy()
    df = df[df["iso3"].str.len() == 3]

    # year range
    df = df[(df["year"] >= YEARS_MIN) & (df["year"] <= YEARS_MAX)].reset_index(drop=True)
    return df


def main():
    frames = []

    for col, code in WB_IND.items():
        print(f"[Q4A] Fetching WB {col} ({code}) ...")
        frames.append(fetch_wb_indicator_long(code, col))

    wb = frames[0]
    for f in frames[1:]:
        wb = wb.merge(f, on=["iso3", "year"], how="outer")

    owid = fetch_owid_co2()

    # Merge WB + OWID on iso3/year
    df = wb.merge(owid, on=["iso3", "year"], how="left")

    # Basic sanity + missingness
    df = df.sort_values(["iso3", "year"]).reset_index(drop=True)
    miss = (df[["gdp_current_usd", "population", "co2_mt", "co2_per_capita"]].isna().mean() * 100).round(1)

    print(f"[Q4A] Panel rows: {len(df)} | Countries: {df['iso3'].nunique()} | Years: ({int(df.year.min())},{int(df.year.max())})")
    print("[Q4A] Missingness (%):")
    for k, v in miss.items():
        print(f"  - {k}: {v}%")

    df.to_parquet(OUT, index=False)
    print("\nSaved:", OUT)


if __name__ == "__main__":
    main()


