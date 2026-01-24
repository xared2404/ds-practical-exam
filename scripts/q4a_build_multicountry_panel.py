from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"

# Ruta A debe leer el panel grande (WB + OWID)
INPATH = DATA / "q4a_panel_country_year.parquet"
OUTPATH = DATA / "q4a_multicountry_panel.parquet"

# Coverage guardrails (ajustables)
YEAR_MIN = 1990
YEAR_MAX = 2023
MIN_YEARS_PER_COUNTRY = 20  # mínimo de años con datos completos por país

REQUIRED_COLS = {
    "iso3",
    "year",
    "gdp_current_usd",
    "population",
    # alguno de estos debe existir:
    # "co2_per_capita" (preferido) o "co2_mt" (alternativo)
}


def main():
    if not INPATH.exists():
        raise SystemExit(
            f"[Q4A] Missing input: {INPATH}\n"
            "Primero corre:\n"
            "  PYTHONPATH=src python scripts/q4a_fetch_panel_all.py"
        )

    print("Root:", ROOT)
    print("Reading:", INPATH)
    df = pd.read_parquet(INPATH)

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise SystemExit(
            f"[Q4A] Input panel missing required columns: {sorted(missing)}"
        )

    if "co2_per_capita" not in df.columns and "co2_mt" not in df.columns:
        raise SystemExit(
            "[Q4A] Input must contain at least one of: co2_per_capita, co2_mt.\n"
            f"Columns: {df.columns.tolist()}"
        )

    # ---- Basic cleaning ----
    df = df.replace([np.inf, -np.inf], np.nan).copy()
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["iso3", "year"]).copy()
    df["year"] = df["year"].astype(int)

    # restrict years
    df = df[(df["year"] >= YEAR_MIN) & (df["year"] <= YEAR_MAX)].copy()

    # co2_per_capita: prefer if available, else compute from co2_mt + population
    # co2_mt should be "million tonnes". If you have "co2_kt", convert to mt first.
    if "co2_per_capita" not in df.columns or df["co2_per_capita"].isna().mean() > 0.95:
        # try to build co2_per_capita if possible
        if "co2_mt" in df.columns:
            # tons per person: (Mt * 1e6) / pop
            df["co2_per_capita"] = (
                pd.to_numeric(df["co2_mt"], errors="coerce") * 1e6
            ) / pd.to_numeric(df["population"], errors="coerce")
        else:
            raise SystemExit("[Q4A] Cannot compute co2_per_capita (missing co2_mt).")

    # ensure numeric
    num_cols = ["gdp_current_usd", "population", "co2_per_capita"]
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # ---- Drop rows missing core signals ----
    df = df.dropna(
        subset=["iso3", "year", "gdp_current_usd", "population", "co2_per_capita"]
    ).copy()

    # ---- Coverage filter: keep countries with enough usable years ----
    years_per_iso = df.groupby("iso3")["year"].nunique().sort_values(ascending=False)
    keep_iso = years_per_iso[years_per_iso >= MIN_YEARS_PER_COUNTRY].index
    df = df[df["iso3"].isin(keep_iso)].copy()

    # Sort + final sanity
    df = df.sort_values(["iso3", "year"]).reset_index(drop=True)

    # Keep only the columns downstream expects (but keep country name if exists)
    keep_cols = [
        "country",
        "iso3",
        "year",
        "gdp_current_usd",
        "population",
        "co2_per_capita",
    ]
    if "country" not in df.columns:
        keep_cols.remove("country")
    df = df[keep_cols].copy()

    OUTPATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUTPATH, index=False)

    print("Saved:", OUTPATH)
    print("Final panel shape:", df.shape)
    print("Countries:", df["iso3"].nunique(), "| Years:", df["year"].nunique())
    print("Years range:", (int(df["year"].min()), int(df["year"].max())))


if __name__ == "__main__":
    main()
