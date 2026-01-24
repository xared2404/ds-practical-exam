"""
Q5 Prioritization Ranking
Run:
  PYTHONPATH=src python scripts/q5_prioritization.py

Inputs (from Q4):
  data/processed/q4_features.parquet

Outputs:
  data/processed/q5_country_ranking.csv
  reports/Q5_ranking.md
"""

from pathlib import Path
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"

def load_features():
    path = DATA / "q4_features.parquet"
    if not path.exists():
        raise SystemExit(f"[Q5] Missing input: {path}\nRun Q4 first to generate q4_features.parquet.")
    print("Reading:", path)
    df = pd.read_parquet(path)

    # sanity
    needed = {"iso3","year","target"}
    if not needed.issubset(df.columns):
        raise SystemExit(f"[Q5] q4_features.parquet missing required columns: {needed - set(df.columns)}")

    df = df.replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)
    return df

def train_rf(X, y):
    rf = RandomForestClassifier(
        n_estimators=400,
        max_depth=6,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )
    rf.fit(X, y)
    return rf

def make_ranking(df, recent_years=5):
    feat_cols = [c for c in df.columns if c not in ("iso3","year","target")]
    X = df[feat_cols].copy()
    y = df["target"].astype(int)

    print("Feature matrix:", X.shape, "| y balance:", y.value_counts().to_dict())
    model = train_rf(X, y)

    # predicted probabilities for class=1 (transition)
    prob = model.predict_proba(X)[:, 1]
    pred = (prob >= 0.5).astype(int)

    df_scored = df[["iso3","year","target"]].copy()
    df_scored["p_transition"] = prob
    df_scored["pred_transition"] = pred

    # recent window per country (last N years available per iso3)
    def last_n(g, n):
        return g.sort_values("year").tail(n)

    rows = []
    for iso, g in df_scored.groupby("iso3", sort=True):
        g = g.sort_values("year")
        g_recent = last_n(g, recent_years)

        # dynamic signal (if available in df)
        dyn = df.loc[g_recent.index]
        dco2 = dyn["d_co2_per_capita"].mean() if "d_co2_per_capita" in dyn.columns else np.nan
        dint = dyn["d_ln_co2_intensity"].mean() if "d_ln_co2_intensity" in dyn.columns else np.nan
        dgdp = dyn["d_ln_gdp_pc"].mean() if "d_ln_gdp_pc" in dyn.columns else np.nan

        latest = g.iloc[-1]

        row = {
            "iso3": iso,
            "latest_year": int(latest["year"]),
            "latest_p_transition": float(latest["p_transition"]),
            "latest_pred_transition": int(latest["pred_transition"]),
            "avg_p_transition_all": float(g["p_transition"].mean()),
            "avg_p_transition_recentN": float(g_recent["p_transition"].mean()),
            "n_years_all": int(len(g)),
            "n_years_recentN": int(len(g_recent)),
            "avg_d_co2_per_capita_recentN": float(dco2) if pd.notna(dco2) else np.nan,
            "avg_d_ln_co2_intensity_recentN": float(dint) if pd.notna(dint) else np.nan,
            "avg_d_ln_gdp_pc_recentN": float(dgdp) if pd.notna(dgdp) else np.nan,
        }
        rows.append(row)

    rank = pd.DataFrame(rows)

    # Composite score (simple + interpretable):
    # prioritize high transition probability AND already-declining emissions dynamics
    # (lower d_co2_per_capita is better => subtract it with a minus sign)
    score = rank["avg_p_transition_recentN"].copy()
    if "avg_d_co2_per_capita_recentN" in rank.columns:
        # normalize dynamics to comparable scale (robust)
        v = rank["avg_d_co2_per_capita_recentN"].astype(float)
        if v.notna().sum() >= 3:
            med = np.nanmedian(v)
            mad = np.nanmedian(np.abs(v - med)) + 1e-9
            z = (v - med) / mad
            # lower d_co2 => better, so subtract z
            score = score - 0.10 * z

    rank["priority_score"] = score

    # rank high to low
    rank = rank.sort_values(["priority_score","avg_p_transition_recentN","latest_p_transition"], ascending=False).reset_index(drop=True)
    rank["rank"] = np.arange(1, len(rank) + 1)

    return df_scored, rank

def to_markdown(rank, outpath_md, top_k=25):
    cols = [
        "rank","iso3","priority_score",
        "avg_p_transition_recentN","latest_year","latest_p_transition",
        "avg_d_co2_per_capita_recentN"
    ]
    view = rank[cols].copy()
    view["priority_score"] = view["priority_score"].map(lambda x: f"{x:.3f}")
    view["avg_p_transition_recentN"] = view["avg_p_transition_recentN"].map(lambda x: f"{x:.3f}")
    view["latest_p_transition"] = view["latest_p_transition"].map(lambda x: f"{x:.3f}")
    view["avg_d_co2_per_capita_recentN"] = view["avg_d_co2_per_capita_recentN"].map(lambda x: "" if pd.isna(x) else f"{x:.3f}")

    md = []
    md.append("# Q5 Country Prioritization Ranking\n")
    md.append("This table ranks countries using a simple, interpretable composite score based on:\n")
    md.append("- Average predicted probability of transition in the most recent window (primary driver)\n")
    md.append("- Recent emissions dynamics (`d_co2_per_capita`) as a secondary adjustment\n")
    md.append("\n")
    md.append(view.head(top_k).to_markdown(index=False))
    md.append("\n")
    outpath_md.write_text("\n".join(md), encoding="utf-8")

def main():
    df = load_features()

    # pick recent window = 5 years by default
    df_scored, rank = make_ranking(df, recent_years=5)

    out_csv = DATA / "q5_country_ranking.csv"
    out_md = REPORTS / "Q5_ranking.md"
    REPORTS.mkdir(parents=True, exist_ok=True)

    rank.to_csv(out_csv, index=False)
    to_markdown(rank, out_md, top_k=30)

    print("\nSaved:", out_csv)
    print("Saved:", out_md)
    print("\nTop 10:\n", rank[["rank","iso3","priority_score","avg_p_transition_recentN","latest_year","latest_p_transition"]].head(10))

if __name__ == "__main__":
    main()
