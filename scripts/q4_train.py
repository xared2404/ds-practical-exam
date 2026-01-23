# scripts/q4_train.py
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
OUT  = DATA


# -----------------------
# I/O
# -----------------------
def load_data():
    path = DATA / "q4_features.parquet"
    print("Reading:", path)
    df = pd.read_parquet(path)

    # Basic sanity
    req = {"iso3", "year", "target"}
    missing = req - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in q4_features.parquet: {missing}")

    df = df.sort_values(["year", "iso3"]).reset_index(drop=True)
    return df


# -----------------------
# Split logic (rolling)
# -----------------------
def rolling_splits(df, min_train_years=10, test_window=5, min_test_n=10):
    """
    Walk-forward evaluation:
      - train: all years <= cutoff
      - test:  cutoff < year <= cutoff+test_window
    We iterate cutoff over time (by unique years).

    We also require:
      - test has BOTH classes (0 and 1)
      - test has at least min_test_n samples
      - train has at least min_train_years unique years
    """
    years = sorted(df["year"].unique())

    splits = []
    for cutoff in years:
        train = df[df["year"] <= cutoff]
        test  = df[(df["year"] > cutoff) & (df["year"] <= cutoff + test_window)]

        if train["year"].nunique() < min_train_years:
            continue
        if len(test) < min_test_n:
            continue

        vc = test["target"].value_counts().to_dict()
        if set(vc.keys()) != {0, 1}:
            continue

        splits.append((cutoff, train.copy(), test.copy(), vc))

    return splits


def featurize(train, test):
    drop_cols = ["iso3", "year", "target"]
    X_train = train.drop(columns=drop_cols)
    y_train = train["target"].astype(int)

    X_test = test.drop(columns=drop_cols)
    y_test = test["target"].astype(int)

    meta_test = test[["iso3", "year"]].copy()
    return X_train, X_test, y_train, y_test, meta_test


# -----------------------
# Models
# -----------------------
def build_models():
    logit = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=2000, class_weight="balanced"))
    ])

    rf = RandomForestClassifier(
        n_estimators=500,
        max_depth=6,
        random_state=42,
        class_weight="balanced_subsample"
    )

    return {
        "LogisticRegression": logit,
        "RandomForest": rf,
    }


# -----------------------
# Evaluation
# -----------------------
def compute_metrics(y_true, y_pred):
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        # helpful for debugging small tests
        "tn": int(confusion_matrix(y_true, y_pred, labels=[0,1])[0,0]),
        "fp": int(confusion_matrix(y_true, y_pred, labels=[0,1])[0,1]),
        "fn": int(confusion_matrix(y_true, y_pred, labels=[0,1])[1,0]),
        "tp": int(confusion_matrix(y_true, y_pred, labels=[0,1])[1,1]),
    }


def main():
    df = load_data()

    # --- Rolling configuration ---
    MIN_TRAIN_YEARS = 10
    TEST_WINDOW     = 5   # years ahead per split
    MIN_TEST_N      = 10

    splits = rolling_splits(
        df,
        min_train_years=MIN_TRAIN_YEARS,
        test_window=TEST_WINDOW,
        min_test_n=MIN_TEST_N,
    )

    if not splits:
        raise SystemExit(
            "[Q4] No valid rolling splits found. "
            "Try decreasing MIN_TRAIN_YEARS, TEST_WINDOW, or MIN_TEST_N."
        )

    print(f"[Q4] Rolling splits found: {len(splits)} "
          f"(min_train_years={MIN_TRAIN_YEARS}, test_window={TEST_WINDOW})")

    models = build_models()

    metrics_by_split = []
    all_preds = []

    # -----------------------
    # Walk-forward loop
    # -----------------------
    for split_id, (cutoff, train, test, test_vc) in enumerate(splits, start=1):
        X_train, X_test, y_train, y_test, meta_test = featurize(train, test)

        print(f"\n[Q4] Split {split_id}: cutoff={cutoff} "
              f"| train_n={len(train)} test_n={len(test)} "
              f"| test_balance={test_vc}")

        for name, model in models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            m = compute_metrics(y_test, y_pred)
            m.update({
                "model": name,
                "split_id": split_id,
                "cutoff_year": int(cutoff),
                "test_start_year": int(cutoff + 1),
                "test_end_year": int(cutoff + TEST_WINDOW),
                "train_n": int(len(train)),
                "test_n": int(len(test)),
                "test_pos": int(test_vc.get(1, 0)),
                "test_neg": int(test_vc.get(0, 0)),
            })
            metrics_by_split.append(m)

            preds = meta_test.copy()
            preds["split_id"] = split_id
            preds["cutoff_year"] = int(cutoff)
            preds["y_true"] = y_test.values
            preds[f"pred_{name}"] = y_pred
            all_preds.append(preds)

    # -----------------------
    # Aggregate metrics
    # -----------------------
    metrics_by_split_df = pd.DataFrame(metrics_by_split)

    summary = (
        metrics_by_split_df
        .groupby("model", as_index=False)[["accuracy", "precision", "recall", "f1"]]
        .mean()
        .sort_values("f1", ascending=False)
        .reset_index(drop=True)
    )

    # merge predictions side-by-side per model
    preds_long = pd.concat(all_preds, ignore_index=True)
    # pivot to have one row per (iso3, year, split_id, cutoff_year) with multiple model preds
    preds_wide = (
        preds_long
        .pivot_table(
            index=["iso3", "year", "split_id", "cutoff_year", "y_true"],
            values=[c for c in preds_long.columns if c.startswith("pred_")],
            aggfunc="first"
        )
        .reset_index()
        .sort_values(["split_id", "iso3", "year"])
    )

    # -----------------------
    # Save outputs
    # -----------------------
    out_summary = OUT / "q4_model_metrics.csv"
    out_splits  = OUT / "q4_model_metrics_by_split.csv"
    out_preds   = OUT / "q4_predictions.csv"

    summary.to_csv(out_summary, index=False)
    metrics_by_split_df.to_csv(out_splits, index=False)
    preds_wide.to_csv(out_preds, index=False)

    print("\nSaved:")
    print(" -", out_summary)
    print(" -", out_splits)
    print(" -", out_preds)

    print("\n[Q4] Average metrics across rolling splits:")
    print(summary)


if __name__ == "__main__":
    main()


