# scripts/q4a_features.py
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"

INPATH = DATA / "q4a_multicountry_panel.parquet"
OUTPATH = DATA / "q4a_features.parquet"

EPS = 1e-12

def _pick(df: pd.DataFrame, options):
    for c in options:
        if c in df.columns:
            return c
    return None

def main():
    if not INPATH.exists():
        raise SystemExit(f"[Q4A] Missing input: {INPATH}")

    print("Reading:", INPATH)
    df = pd.read_parquet(INPATH).copy()

    if not {"iso3", "year"}.issubset(df.columns):
        raise SystemExit(f"[Q4A] Missing iso3/year in panel. Columns={df.columns.tolist()}")

    # Types / cleaning
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df = df.replace([np.inf, -np.inf], np.nan)

    # Column mapping (robust)
    col_gdp = _pick(df, ["gdp_current_usd", "gdp", "ny_gdp_mktp_kd", "ny_gdp_mktp_cd"])
    col_pop = _pick(df, ["population", "sp_pop_totl"])
    col_co2pc = _pick(df, ["co2_per_capita", "en_atm_co2e_pc"])

    if col_gdp is None or col_pop is None or col_co2pc is None:
        raise SystemExit(
            "[Q4A] Could not find gdp/pop/co2_per_capita columns.\n"
            f"Found: gdp={col_gdp}, pop={col_pop}, co2pc={col_co2pc}\n"
            f"Columns: {df.columns.tolist()}"
        )

    # Canonical numeric columns
    df["gdp"] = pd.to_numeric(df[col_gdp], errors="coerce")
    df["population"] = pd.to_numeric(df[col_pop], errors="coerce")
    df["co2_per_capita"] = pd.to_numeric(df[col_co2pc], errors="coerce")

    # Basic sanity drops before ratios/logs
    df = df.dropna(subset=["iso3", "year", "gdp", "population", "co2_per_capita"]).copy()
    df["year"] = df["year"].astype(int)

    # Guardrails against zero/negative
    df["gdp"] = df["gdp"].clip(lower=EPS)
    df["population"] = df["population"].clip(lower=EPS)

    # Derived measures
    df["gdp_pc"] = df["gdp"] / df["population"]
    df["gdp_pc"] = df["gdp_pc"].clip(lower=EPS)

    # NOTE: co2_intensity defined as CO2 per cap over GDP per cap (proxy)
    df["co2_intensity"] = df["co2_per_capita"] / (df["gdp_pc"] + EPS)
    df["co2_intensity"] = df["co2_intensity"].clip(lower=EPS)

    # Logs
    df["ln_gdp"] = np.log(df["gdp"])
    df["ln_population"] = np.log(df["population"])
    df["ln_gdp_pc"] = np.log(df["gdp_pc"])
    df["ln_co2_intensity"] = np.log(df["co2_intensity"])

    # Sort for group operations
    df = df.sort_values(["iso3", "year"]).reset_index(drop=True)

    # -----------------------------
    # TARGET (forward-looking, no leak)
    # -----------------------------
    # 5-year ahead CO2 per capita
    H = 5
    df["co2_pc_lead5"] = df.groupby("iso3")["co2_per_capita"].shift(-H)

    # target=1 if CO2pc falls by >=10% over next 5 years
    df["target"] = (df["co2_pc_lead5"] <= 0.9 * df["co2_per_capita"]).astype(int)

    # drop rows without future outcome
    df = df.dropna(subset=["co2_pc_lead5"]).copy()

    # -----------------------------
    # FEATURES (use only info up to t)
    # -----------------------------
    # contemporaneous diffs become LEAKY if target uses same-year movement;
    # we use lag-1 differences (information available at time t)
    df["d_ln_gdp_pc_lag1"] = df.groupby("iso3")["ln_gdp_pc"].diff(1)
    df["d_co2_per_capita_lag1"] = df.groupby("iso3")["co2_per_capita"].diff(1)
    df["d_ln_co2_intensity_lag1"] = df.groupby("iso3")["ln_co2_intensity"].diff(1)

    # normalized time trend
    y0, y1 = int(df["year"].min()), int(df["year"].max())
    df["year_norm"] = (df["year"] - y0) / (y1 - y0 + 1e-9)

    feature_cols = [
        "ln_gdp",
        "ln_population",
        "ln_gdp_pc",
        "co2_per_capita",
        "ln_co2_intensity",
        "d_ln_gdp_pc_lag1",
        "d_co2_per_capita_lag1",
        "d_ln_co2_intensity_lag1",
        "year_norm",
    ]
    keep_cols = ["iso3", "year", "target"] + feature_cols

    # Final clean matrix
    df_feat = (
        df[keep_cols]
        .replace([np.inf, -np.inf], np.nan)
        .dropna()
        .reset_index(drop=True)
    )

    OUTPATH.parent.mkdir(parents=True, exist_ok=True)
    df_feat.to_parquet(OUTPATH, index=False)

    print("Saved:", OUTPATH)
    print("Final feature matrix shape:", df_feat.shape)
    print("Countries:", df_feat["iso3"].nunique())
    print("Class balance:", df_feat["target"].value_counts().to_dict())
    print("Years range:", (int(df_feat["year"].min()), int(df_feat["year"].max())))

if __name__ == "__main__":
    main()


