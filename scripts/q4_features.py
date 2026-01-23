import os
import numpy as np
import pandas as pd

def find_repo_root():
    root = os.getcwd()
    while root != "/" and not os.path.isdir(os.path.join(root, "data")):
        root = os.path.dirname(root)
    return root

def safe_log(x):
    x = pd.to_numeric(x, errors="coerce")
    return np.log(x.replace([0, np.inf, -np.inf], np.nan))

def main():
    root = find_repo_root()
    inpath = os.path.join(root, "data", "processed", "q4_multicountry_panel.parquet")
    outpath = os.path.join(root, "data", "processed", "q4_features.parquet")

    print("Reading:", inpath)
    df = pd.read_parquet(inpath).sort_values(["iso3", "year"]).reset_index(drop=True)

    required = ["iso3","year","gdp_current_usd","population","co2_mt","co2_per_capita"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Missing required columns: {missing}\nAvailable: {list(df.columns)}")

    df["ln_gdp"] = safe_log(df["gdp_current_usd"])
    df["ln_population"] = safe_log(df["population"])

    df["gdp_pc"] = df["gdp_current_usd"] / df["population"]
    df["ln_gdp_pc"] = safe_log(df["gdp_pc"])

    # target: decoupling year (GDPpc up, CO2pc down)
    df["ln_gdp_pc_lag1"] = df.groupby("iso3")["ln_gdp_pc"].shift(1)
    df["co2_pc_lag1"] = df.groupby("iso3")["co2_per_capita"].shift(1)
    df["d_ln_gdp_pc"] = df["ln_gdp_pc"] - df["ln_gdp_pc_lag1"]
    df["d_co2_per_capita"] = df["co2_per_capita"] - df["co2_pc_lag1"]
    df["target"] = ((df["d_ln_gdp_pc"] > 0) & (df["d_co2_per_capita"] < 0)).astype(int)

    df["co2_intensity"] = df["co2_mt"] / df["gdp_current_usd"]
    df["ln_co2_intensity"] = safe_log(df["co2_intensity"])

    df["ln_co2_intensity_lag1"] = df.groupby("iso3")["ln_co2_intensity"].shift(1)
    df["d_ln_co2_intensity"] = df["ln_co2_intensity"] - df["ln_co2_intensity_lag1"]

    df["year_norm"] = (df["year"] - df["year"].mean()) / df["year"].std()

    feature_cols = [
        "ln_gdp","ln_population","ln_gdp_pc","co2_per_capita","ln_co2_intensity",
        "d_ln_gdp_pc","d_co2_per_capita","d_ln_co2_intensity","year_norm"
    ]
    keep_cols = ["iso3","year","target"] + feature_cols

    df_feat = df[keep_cols].replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)

    print("Final feature matrix shape:", df_feat.shape)
    print("Class balance:", df_feat["target"].value_counts().to_dict())
    print("Saving:", outpath)
    df_feat.to_parquet(outpath, index=False)
    print("Saved:", outpath)

if __name__ == "__main__":
    main()
