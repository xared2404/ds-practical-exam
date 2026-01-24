from pathlib import Path
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"

INPATH = DATA / "q4a_features.parquet"
OUT_METRICS = DATA / "q4a_model_metrics.csv"
OUT_BY_SPLIT = DATA / "q4a_model_metrics_by_split.csv"
OUT_PREDS = DATA / "q4a_predictions.csv"


def rolling_cutoffs(df, min_train_years=10, test_window=5):
    years = sorted(df["year"].unique())
    first, last = years[0], years[-1]
    cutoffs = []
    for cutoff in years:
        train_years = cutoff - first + 1
        if train_years < min_train_years:
            continue
        if cutoff + test_window > last:
            continue
        cutoffs.append(cutoff)
    return cutoffs


def eval_row(model_name, split_id, cutoff, y_true, y_pred):
    return {
        "split": split_id,
        "cutoff_year": cutoff,
        "model": model_name,
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "test_n": int(len(y_true)),
        "test_0": int((y_true == 0).sum()),
        "test_1": int((y_true == 1).sum()),
    }


def main():
    if not INPATH.exists():
        raise SystemExit(f"[Q4A] Missing input: {INPATH}")

    print("Reading:", INPATH)
    df = pd.read_parquet(INPATH).sort_values(["year", "iso3"]).reset_index(drop=True)
    feat_cols = [c for c in df.columns if c not in ("iso3", "year", "target")]

    cutoffs = rolling_cutoffs(df, min_train_years=10, test_window=5)
    print(f"[Q4A] Rolling splits found: {len(cutoffs)}")
    if not cutoffs:
        raise SystemExit("[Q4A] Not enough years to do rolling validation.")

    models = {
        "LogisticRegression": Pipeline(
            [("scaler", StandardScaler()), ("clf", LogisticRegression(max_iter=2000))]
        ),
        "RandomForest": RandomForestClassifier(
            n_estimators=400,
            max_depth=6,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1,
        ),
    }

    metrics_rows = []
    preds_rows = []

    for i, cutoff in enumerate(cutoffs, start=1):
        train = df[df["year"] <= cutoff].copy()
        test = df[(df["year"] > cutoff) & (df["year"] <= cutoff + 5)].copy()

        X_train, y_train = train[feat_cols], train["target"].astype(int).values
        X_test, y_test = test[feat_cols], test["target"].astype(int).values

        bal = pd.Series(y_test).value_counts().to_dict()
        print(
            f"[Q4A] Split {i}: cutoff={cutoff} train_n={len(train)} test_n={len(test)} test_balance={bal}"
        )

        for name, mdl in models.items():
            mdl.fit(X_train, y_train)
            y_pred = mdl.predict(X_test)

            metrics_rows.append(eval_row(name, i, cutoff, y_test, y_pred))

            out = test[["iso3", "year"]].copy()
            out["split"] = i
            out["cutoff_year"] = cutoff
            out["model"] = name
            out["y_true"] = y_test
            out["y_pred"] = y_pred
            preds_rows.append(out)

    metrics = pd.DataFrame(metrics_rows)
    preds = pd.concat(preds_rows, axis=0, ignore_index=True)
    avg = (
        metrics.groupby("model")[["accuracy", "precision", "recall", "f1"]]
        .mean()
        .reset_index()
    )

    OUT_METRICS.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(OUT_BY_SPLIT, index=False)
    preds.to_csv(OUT_PREDS, index=False)
    avg.to_csv(OUT_METRICS, index=False)

    print("Saved:")
    print(" -", OUT_METRICS)
    print(" -", OUT_BY_SPLIT)
    print(" -", OUT_PREDS)
    print("\n[Q4A] Average across splits:\n", avg.sort_values("f1", ascending=False))


if __name__ == "__main__":
    main()
