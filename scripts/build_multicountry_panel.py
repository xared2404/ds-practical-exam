# scripts/build_multicountry_panel.py

import os
import pandas as pd
import numpy as np

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_PROCESSED = os.path.join(ROOT, "data", "processed")

INFILE = os.path.join(DATA_PROCESSED, "panel_country_year.parquet")
OUTFILE = os.path.join(DATA_PROCESSED, "q4_multicountry_panel.parquet")

START_YEAR = 1995


def build_panel():
    print("Root:", ROOT)
    print("Reading:", INFILE)

    df = pd.read_parquet(INFILE)

    # --------------------------------------------------
    # Keep wider country set if available
    # (Q1–Q3 used MEX/USA; Q4 generalizes)
    # --------------------------------------------------
    df = df[df["year"] >= START_YEAR].copy()

    # --------------------------------------------------
    # Growth rates and differences
    # --------------------------------------------------
    df = df.sort_values(["iso3", "year"])

    df["gdp_growth"] = df.groupby("iso3")["gdp_current_usd"].pct_change()
    df["co2_pc_change"] = df.groupby("iso3")["co2_per_capita"].diff()

    # --------------------------------------------------
    # Classification target:
    # Decoupling event
    # --------------------------------------------------
    df["decoupling_event"] = (
        (df["gdp_growth"] > 0) & (df["co2_pc_change"] < 0)
    ).astype(int)

    # --------------------------------------------------
    # Drop first differences & missing
    # --------------------------------------------------
    keep_cols = [
        "iso3",
        "year",
        "gdp_current_usd",
        "population",
        "co2_mt",
        "co2_per_capita",
        "gdp_growth",
        "co2_pc_change",
        "decoupling_event",
    ]

    df_out = (
        df[keep_cols].replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)
    )

    print("Final panel shape:", df_out.shape)
    print("Class balance:", df_out["decoupling_event"].value_counts().to_dict())

    df_out.to_parquet(OUTFILE, index=False)
    print("Saved:", OUTFILE)


if __name__ == "__main__":
    build_panel()
