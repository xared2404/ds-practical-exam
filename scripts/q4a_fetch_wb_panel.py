"""
Q4A - Fetch full multi-country panel from World Bank API (ALL available countries, excluding aggregates)

Run:
  PYTHONPATH=src python scripts/q4a_fetch_wb_panel.py

Outputs:
  data/processed/q4a_panel_country_year.parquet

Notes:
- Pulls ALL WB countries except those with region == "Aggregates".
- Years: 1990-2023 (editable below)
- Indicators:
    GDP (current US$):        NY.GDP.MKTP.CD
    Population:              SP.POP.TOTL
    CO2 emissions (kt):      EN.ATM.CO2E.KT
    CO2 emissions per capita EN.ATM.CO2E.PC
- Builds a wide panel with columns:
    iso3, country, year, gdp_current_usd, population, co2_kt, co2_mt, co2_per_capita
"""

from __future__ import annotations
from pathlib import Path
import time
import json
import math
import requests
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
OUT = DATA / "q4a_panel_country_year.parquet"

WB = "https://api.worldbank.org/v2"

YEARS_MIN = 1990
YEARS_MAX = 2023

INDICATORS = {
    "gdp_current_usd": "NY.GDP.MKTP.CD",
    "population": "SP.POP.TOTL",
    "co2_kt": "EN.ATM.CO2E.KT",
    "co2_per_capita": "EN.ATM.CO2E.PC",
}

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "ds-practical-exam-q4a/1.0"})


def _get_json(
    url: str, params: dict | None = None, retries: int = 5, backoff: float = 1.2
):
    last_err = None
    for i in range(retries):
        try:
            r = SESSION.get(url, params=params, timeout=60)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last_err = e
            time.sleep(backoff ** (i + 1))
    raise RuntimeError(
        f"[WB] Failed after {retries} retries: {url}\nLast error: {last_err}"
    )


def fetch_all_countries() -> pd.DataFrame:
    # World Bank countries list is paginated
    per_page = 400
    page = 1
    rows = []

    while True:
        url = f"{WB}/country"
        js = _get_json(
            url, params={"format": "json", "per_page": per_page, "page": page}
        )
        meta, data = js[0], js[1]
        for c in data:
            # Exclude aggregates
            if (c.get("region") or {}).get("value") == "Aggregates":
                continue
            iso3 = c.get("id")
            name = c.get("name")
            if not iso3 or iso3.strip() == "":
                continue
            rows.append({"iso3": iso3, "country": name})
        if page >= int(meta.get("pages", 1)):
            break
        page += 1

    df = pd.DataFrame(rows).drop_duplicates().sort_values("iso3").reset_index(drop=True)
    print(f"[Q4A] Countries fetched (non-aggregates): {len(df)}")
    return df


def fetch_indicator_long(
    indicator_code: str, value_name: str, years_min: int, years_max: int
) -> pd.DataFrame:
    """
    Robust WB fetch: handles non-standard responses:
      - [] (empty)
      - {"message":[...]} (errors)
      - [meta] without data (throttling)
    Returns empty DF if indicator/page unavailable.
    """
    import time

    per_page = 20000
    page = 1
    out = []
    date = f"{years_min}:{years_max}"

    while True:
        url = f"{WB}/country/all/indicator/{indicator_code}"

        # retry loop for transient WB glitches/throttling
        js = None
        for attempt in range(5):
            js = _get_json(
                url,
                params={
                    "format": "json",
                    "per_page": per_page,
                    "page": page,
                    "date": date,
                },
            )

            ok = isinstance(js, list) and len(js) >= 2 and isinstance(js[0], dict)
            if ok:
                break

            # non-standard payload; backoff and retry
            wait = 0.75 * (2**attempt)
            print(
                f"[Q4A] WARNING: Non-standard WB response for {indicator_code} page={page} (attempt {attempt+1}/5). Backoff {wait:.1f}s"
            )
            try:
                preview = str(js)[:200]
            except Exception:
                preview = "<unprintable>"
            print(f"[Q4A] Preview: {preview}")
            time.sleep(wait)

        # if still not ok, stop gracefully (no crash)
        if not (isinstance(js, list) and len(js) >= 2):
            print(
                f"[Q4A] ERROR: Giving up on {indicator_code} page={page}. Returning empty/partial data."
            )
            break

        meta, data = js[0], js[1]

        if data is None:
            break

        # data sometimes comes as dict with message
        if isinstance(data, dict) and "message" in data:
            print(
                f"[Q4A] WARNING: WB message for {indicator_code}: {data.get('message')}"
            )
            break

        if not isinstance(data, list) or len(data) == 0:
            break

        for r in data:
            iso3 = r.get("countryiso3code")
            year = r.get("date")
            val = r.get("value")
            if not iso3 or not year:
                continue
            try:
                y = int(year)
            except Exception:
                continue
            out.append({"iso3": iso3, "year": y, value_name: val})

        pages = int(meta.get("pages", 1)) if isinstance(meta, dict) else 1
        if page >= pages:
            break
        page += 1

    df = pd.DataFrame(out)
    if df.empty:
        return pd.DataFrame(columns=["iso3", "year", value_name])

    df[value_name] = pd.to_numeric(df[value_name], errors="coerce")
    return df


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    countries = fetch_all_countries()

    longs = []
    for col, code in INDICATORS.items():
        print(f"[Q4A] Fetching indicator {col} ({code}) ...")
        dfi = fetch_indicator_long(code, col, YEARS_MIN, YEARS_MAX)
        longs.append(dfi)

    # Merge all indicators on iso3-year
    df = longs[0]
    for dfi in longs[1:]:
        df = df.merge(dfi, on=["iso3", "year"], how="outer")

    # Keep only real countries (exclude aggregates again via join)
    df = df.merge(countries, on="iso3", how="inner")

    # Compute co2_mt from kt (1 kt = 0.001 Mt)
    if "co2_kt" in df.columns:
        df["co2_mt"] = df["co2_kt"] / 1000.0
    else:
        df["co2_mt"] = np.nan

    # Clean and order
    df = (
        df[
            [
                "iso3",
                "country",
                "year",
                "gdp_current_usd",
                "population",
                "co2_kt",
                "co2_mt",
                "co2_per_capita",
            ]
        ]
        .sort_values(["iso3", "year"])
        .reset_index(drop=True)
    )

    # Basic coverage report
    n_c = df["iso3"].nunique()
    yrs = (int(df["year"].min()), int(df["year"].max()))
    print(f"[Q4A] Panel rows: {len(df)} | Countries: {n_c} | Years range: {yrs}")
    print("[Q4A] Missingness (%):")
    miss = (
        df[["gdp_current_usd", "population", "co2_mt", "co2_per_capita"]]
        .isna()
        .mean()
        .sort_values(ascending=False)
    )
    for k, v in miss.items():
        print(f"  - {k}: {v*100:.1f}%")

    df.to_parquet(OUT, index=False)
    print("\nSaved:", OUT)


if __name__ == "__main__":
    main()
