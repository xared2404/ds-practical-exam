#!/usr/bin/env python3
"""Genera una figura top-30 de prioridad a partir de data/processed/q5_country_ranking.csv
Guarda la salida en outputs/figures/q5_top30_priority_score.png
"""
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
csv_path = repo_root / "data" / "processed" / "q5_country_ranking.csv"
out_path = repo_root / "outputs" / "figures" / "q5_top30_priority_score.png"

if not csv_path.exists():
    print(f"ERROR: CSV not found: {csv_path}")
    sys.exit(2)

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
except ImportError as e:
    print("ERROR: Missing python package. Please install pandas, matplotlib, seaborn.")
    print("You can install them with: pip install pandas matplotlib seaborn")
    sys.exit(3)

# Read and prepare
df = pd.read_csv(csv_path)
if "priority_score" not in df.columns or "iso3" not in df.columns:
    print("ERROR: CSV does not contain required columns 'iso3' and 'priority_score'")
    sys.exit(4)

# Sort descending and take top 30
df_sorted = df.sort_values("priority_score", ascending=False).head(30)
# Ensure plot directory exists
out_path.parent.mkdir(parents=True, exist_ok=True)

plt.figure(figsize=(8, 10))
sns.set_style("whitegrid")
# horizontal bar for better readability
plt.barh(df_sorted["iso3"][::-1], df_sorted["priority_score"][::-1], color="C0")
plt.xlabel("priority_score")
plt.title("Top-30 countries by priority_score (Q5)")
plt.tight_layout()
plt.savefig(out_path, dpi=150)
print(f"Saved figure to {out_path}")
