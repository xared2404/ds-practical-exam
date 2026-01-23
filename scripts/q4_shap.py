# scripts/q4_shap.py
# Run:
#   PYTHONPATH=src python scripts/q4_shap.py
#
# Outputs (saved in data/processed/):
#   q4_shap_summary_dot.png
#   q4_shap_summary_bar.png
#   q4_shap_dependence_top1.png

from pathlib import Path
import warnings

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"


def load_features(max_samples=200):
    path = DATA / "q4_features.parquet"
    print("Reading:", path)
    df = pd.read_parquet(path)

    # y
    y = df["target"].astype(int)

    # X (solo features)
    X = df.drop(columns=["iso3", "year", "target"]).copy()
    X = X.replace([np.inf, -np.inf], np.nan).dropna()
    y = y.loc[X.index]

    # sample para que SHAP sea rápido/estable
    if len(X) > max_samples:
        Xs = X.sample(max_samples, random_state=42)
        ys = y.loc[Xs.index]
    else:
        Xs, ys = X, y

    print("X sample:", Xs.shape, "| y balance:", ys.value_counts().to_dict())
    return Xs, ys


def train_rf(X, y):
    rf = RandomForestClassifier(
        n_estimators=300,
        max_depth=5,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )
    rf.fit(X, y)
    return rf


def main():
    try:
        import shap
    except Exception as e:
        raise SystemExit(
            "\n[Q4] Missing dependency: shap\n"
            "Install inside your venv:\n"
            "  pip install shap\n"
            f"\nOriginal error: {e}\n"
        )

    X, y = load_features(max_samples=200)
    model = train_rf(X, y)

    # Prefer the modern API when available (avoids many shape mismatches)
    # If it fails, fallback to TreeExplainer.
    try:
        explainer = shap.Explainer(model, X)
        exp = explainer(X)

        values = exp.values
        # For binary classification: (n,p) or (n,p,2). If 3D, take class=1.
        if values.ndim == 3:
            sv = values[:, :, 1]
        else:
            sv = values

        X_plot = X

    except Exception:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X)

        # If list -> pick class 1 (positive class)
        if isinstance(shap_values, list):
            sv = shap_values[1]
        else:
            sv = shap_values

        X_plot = X

    # --- Summary (dot) ---
    out_dot = DATA / "q4_shap_summary_dot.png"
    plt.figure()
    shap.summary_plot(sv, X_plot, show=False)
    plt.tight_layout()
    plt.savefig(out_dot, dpi=150)
    plt.close()
    print("Saved:", out_dot)

    # --- Summary (bar) ---
    out_bar = DATA / "q4_shap_summary_bar.png"
    plt.figure()
    shap.summary_plot(sv, X_plot, plot_type="bar", show=False)
    plt.tight_layout()
    plt.savefig(out_bar, dpi=150)
    plt.close()
    print("Saved:", out_bar)

    # --- Dependence (top feature by mean |SHAP|) ---
    out_dep = DATA / "q4_shap_dependence_top1.png"

    # Align SHAP values to feature matrix (defensive)
    p = X_plot.shape[1]
    if sv.ndim != 2:
        sv2 = np.array(sv)
        if sv2.ndim == 3:
            sv2 = sv2[:, :, -1]
        sv = sv2

    sv_aligned = sv[:, :p] if sv.shape[1] >= p else sv
    if sv_aligned.shape[1] != p:
        raise SystemExit(
            f"[Q4] SHAP alignment failed: sv_aligned.shape={sv_aligned.shape}, X_plot.shape={X_plot.shape}"
        )

    mean_abs = np.abs(sv_aligned).mean(axis=0)
    top_idx = int(np.argmax(mean_abs))
    top_feat = X_plot.columns[top_idx]

    plt.figure()
    shap.dependence_plot(top_feat, sv_aligned, X_plot, show=False)
    plt.tight_layout()
    plt.savefig(out_dep, dpi=150)
    plt.close()
    print("Saved:", out_dep)

    print("\n[Q4] SHAP done. Top feature:", top_feat)


if __name__ == "__main__":
    main()
