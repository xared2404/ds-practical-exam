# =========================================================
# Q3.1 – Figures: Historical + Baseline + Scenarios
# =========================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROCESSED = os.path.join(ROOT, "data", "processed")

PANEL_PATH = os.path.join(DATA_PROCESSED, "panel_country_year.parquet")
SCENARIOS_PATH = os.path.join(DATA_PROCESSED, "q3_scenarios_2035.csv")

FIG_MT = os.path.join(DATA_PROCESSED, "q3_scenarios_co2_mt_2035.png")
FIG_PC = os.path.join(DATA_PROCESSED, "q3_scenarios_co2_pc_2035.png")

print("Root:", ROOT)
print("Reading:", PANEL_PATH)
print("Reading:", SCENARIOS_PATH)

# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------
df = pd.read_parquet(PANEL_PATH)
sc = pd.read_csv(SCENARIOS_PATH)


# ---------------------------------------------------------
# Helper function
# ---------------------------------------------------------
def plot_scenarios(
    hist_df, scen_df, y_hist, y_base, y_nodec, y_strong, ylabel, title, outpath
):
    plt.figure(figsize=(9, 6))

    for iso in ["MEX", "USA"]:
        h = hist_df[hist_df["iso3"] == iso]
        s = scen_df[scen_df["iso3"] == iso]

        plt.plot(h["year"], h[y_hist], linewidth=2, label=f"{iso} (historical)")

        plt.plot(
            s["year"], s[y_base], linestyle="--", linewidth=2, label=f"{iso} – baseline"
        )

        plt.plot(
            s["year"],
            s[y_nodec],
            linestyle=":",
            linewidth=2,
            label=f"{iso} – no decoupling",
        )

        plt.plot(
            s["year"],
            s[y_strong],
            linestyle="-.",
            linewidth=2,
            label=f"{iso} – strong decoupling",
        )

    plt.xlabel("Year")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.show()

    print("Saved figure:", outpath)


# ---------------------------------------------------------
# FIGURE 1: CO2 total (Mt)
# ---------------------------------------------------------
plot_scenarios(
    hist_df=df,
    scen_df=sc,
    y_hist="co2_mt",
    y_base="co2_mt_baseline",
    y_nodec="co2_mt_nodec",
    y_strong="co2_mt_strong",
    ylabel="CO₂ emissions (Mt)",
    title="CO₂ emissions: historical data and scenarios (1990–2035)",
    outpath=FIG_MT,
)

# ---------------------------------------------------------
# FIGURE 2: CO2 per capita
# ---------------------------------------------------------
plot_scenarios(
    hist_df=df,
    scen_df=sc,
    y_hist="co2_per_capita",
    y_base="co2_pc_baseline",
    y_nodec="co2_pc_nodec",
    y_strong="co2_pc_strong",
    ylabel="CO₂ emissions per capita (tons/person)",
    title="CO₂ emissions per capita: historical data and scenarios (1990–2035)",
    outpath=FIG_PC,
)

print("Q3.1 figures completed successfully.")
