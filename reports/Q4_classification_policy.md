# Q4. Classification, Explainability, and Policy Implications

## Overview

This section develops a supervised classification framework to identify **emissions regime transitions** across countries. The analysis complements the econometric evidence in Q2 and the scenario projections in Q3 by shifting from prediction of levels to **comparative pattern recognition**.

Rather than producing forecasts, the objective is to:

1. Assess whether recent macro–environmental dynamics can predict transitions in emissions behavior, and  
2. Extract **policy-relevant characteristics** that distinguish countries undergoing successful decarbonization dynamics.

The central business and policy question addressed is:

> *What distinguishes countries that successfully enter emissions-reduction regimes, and how can these insights inform climate policy design elsewhere?*

All results are explicitly interpreted as **scenario-based and comparative**, not causal or predictive in a strict sense.

---

## Q4.1 Multi-Country Panel Construction

The analysis begins from the processed country–year panel used in Q2 and Q3 (1990–2023). This panel is expanded to include multiple countries observed over time and is transformed into a **classification-ready dataset**.

A binary target variable is defined to capture **regime transitions** in emissions dynamics, operationalized as sustained changes in per-capita emissions behavior rather than short-run shocks.

**Final panel characteristics:**
- Unit of analysis: country–year
- Observations: 56 country–year pairs
- Target balance: approximately balanced across classes
- Output: `data/processed/q4_multicountry_panel.parquet`

This structure provides sufficient temporal and cross-sectional variation while preserving interpretability.

---

## Q4.2 Feature Engineering

From the multi-country panel, a compact and interpretable feature set is constructed. Features are designed to capture both **levels** and **dynamics** of economic activity and emissions intensity.

### Feature set

- **Log-levels**
  - `ln_gdp`
  - `ln_population`
  - `ln_gdp_pc`
  - `ln_co2_intensity`

- **Emissions outcomes**
  - `co2_per_capita`

- **First differences (dynamics)**
  - `d_ln_gdp_pc`
  - `d_co2_per_capita`
  - `d_ln_co2_intensity`

- **Normalized time trend**
  - `year_norm`

The inclusion of differenced variables is directly motivated by Q2 and Q3, where **dynamic decoupling effects** were shown to dominate static income effects.

**Output:** `data/processed/q4_features.parquet`

---

## Q4.3 Classification Models and Evaluation Strategy

Two supervised learning models are estimated:

1. **Logistic Regression** (with standardization)  
2. **Random Forest Classifier** (depth-limited, class-weighted)

### Temporal validation (Option B)

Model evaluation follows a **rolling temporal validation strategy**, explicitly designed to respect the time structure of the data and avoid information leakage:

- Minimum training window: 10 years  
- Fixed test window: 5 years  
- Sequential rolling cutoffs evaluated across time

This approach yields multiple out-of-sample evaluations rather than a single arbitrary split.

### Average performance across rolling splits

| Model                | Accuracy | Precision | Recall | F1   |
|---------------------|----------|-----------|--------|------|
| Random Forest       | ≈ 0.85   | ≈ 0.79    | ≈ 0.93 | ≈ 0.82 |
| Logistic Regression | ≈ 0.71   | ≈ 0.70    | ≈ 0.95 | ≈ 0.75 |

The Random Forest consistently outperforms the linear benchmark, indicating the presence of nonlinear interactions and threshold effects.

**Outputs:**
- `q4_model_metrics.csv`
- `q4_model_metrics_by_split.csv`
- `q4_predictions.csv`

---

## Q4.4 Model Explainability with SHAP

To interpret the classification results, SHAP (SHapley Additive exPlanations) is applied to the trained Random Forest model.

SHAP values quantify the marginal contribution of each feature to the predicted probability of an emissions regime transition. These explanations are **model-local and predictive**, not causal.

### Summary results

Two complementary visualizations are produced:

- **SHAP summary (dot) plot** — distribution and direction of feature effects  
- **SHAP summary (bar) plot** — mean absolute feature importance  

Both plots consistently identify **`d_co2_per_capita`** as the most influential feature.

A dependence plot for the top-ranked feature further illustrates how changes in per-capita emissions growth strongly influence regime classification.

**Outputs:**
- `q4_shap_summary_dot.png`
- `q4_shap_summary_bar.png`
- `q4_shap_dependence_top1.png`

---

## Q4.5 Interpretation and Policy Implications

Three key insights emerge.

### 1. Dynamics dominate levels  
The most influential predictor is the *change* in per-capita emissions (`d_co2_per_capita`), rather than GDP, population, or emissions levels. This mirrors Q2, where time effects absorbed much of the income effect once dynamics were accounted for.

### 2. Regime transitions reflect decoupling dynamics  
The classifier detects shifts driven by acceleration or reversal in emissions intensity, not by economic scale. This reinforces Q3, where alternative decoupling assumptions dominated long-run emissions outcomes.

### 3. Policy relevance  
From a policy perspective, the results suggest that **monitoring short-run emissions dynamics** provides earlier and more informative signals than tracking levels alone. Policies that affect emissions growth rates—such as energy transitions, regulatory tightening, or carbon pricing—are more likely to trigger detectable regime changes than policies targeting levels indirectly.

---

## Q4.6 Limitations

Several limitations should be noted:

- The number of countries remains limited, constraining external validity.
- Regime definitions are reduced-form and do not isolate specific policy instruments.
- SHAP explanations describe **predictive contributions**, not causal effects.
- Long-run GDP and population uncertainty is not modeled explicitly.

Accordingly, the results should be interpreted as **illustrative and comparative**, rather than predictive.

---

## Q4.7 Conclusion

Q4 demonstrates that emissions regime transitions can be effectively classified using a small and interpretable set of macro–environmental features. Dynamic emissions indicators consistently outperform static economic variables, and explainability analysis confirms the central role of short-run decoupling dynamics.

Taken together, Q2–Q4 provide a coherent empirical narrative:

> **Economic growth alone does not determine emissions outcomes. What matters is how emissions evolve relative to growth, and how quickly those dynamics change.**
