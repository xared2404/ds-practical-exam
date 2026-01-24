Q4. Classification, Explainability, and Policy Implications

4.1 Objective and Conceptual Framing

This section develops a supervised classification framework to identify emissions regime transitions across countries. The objective is not to forecast emissions levels, but to detect structural changes in emissions dynamics that signal a country’s capacity to sustain decarbonization.

This framing is directly motivated by earlier results:
	•	Q2 showed that time dynamics dominate static income effects in emissions behavior.
	•	Q3 demonstrated that small differences in decoupling rates generate large long-run emissions divergence.

Q4 translates these insights into a policy-relevant classification task: identifying when countries shift into regimes characterized by declining emissions intensity.

⸻

4.2 Target Variable Definition

The binary target variable is defined at the country–year level:
	•	target = 1: per-capita CO₂ emissions decline relative to the previous period
	•	target = 0: otherwise

Formally, the target captures whether a country-year observation exhibits negative growth in per-capita emissions, interpreted as a reduced-form proxy for:
	•	technological upgrading,
	•	institutional capacity,
	•	energy transition policy effectiveness.

This definition is intentionally agnostic about specific policy instruments and instead focuses on observable emissions outcomes, aligning with the reduced-form approach used throughout the exam.

⸻

4.3 Feature Engineering

The feature set is deliberately compact and interpretable, combining levels, dynamics, and temporal structure.

Economic and emissions levels
	•	ln_gdp
	•	ln_population
	•	ln_gdp_pc
	•	co2_per_capita
	•	ln_co2_intensity

Dynamic indicators (first differences)
	•	d_ln_gdp_pc
	•	d_co2_per_capita
	•	d_ln_co2_intensity

Time normalization
	•	year_norm

The emphasis on dynamic variables is directly grounded in Q2 and Q3, where changes over time consistently dominated static income effects.

Output: data/processed/q4_features.parquet

⸻

4.4 Baseline Classification and Temporal Validation

Two classification models are estimated:
	1.	Logistic Regression (interpretable linear benchmark)
	2.	Random Forest Classifier (depth-limited, class-weighted)

Temporal validation strategy

To avoid information leakage, evaluation uses a rolling temporal split:
	•	Expanding training window
	•	Fixed forward test window
	•	Multiple cutoffs evaluated sequentially

This mimics real-time policy monitoring, where only past information is available at prediction time.
## Baseline performance (two-country setup)

| Model               | Accuracy | Precision | Recall | F1   |
|---------------------|----------|-----------|--------|------|
| Random Forest       | ≈ 0.85   | ≈ 0.79    | ≈ 0.93 | ≈ 0.82 |
| Logistic Regression | ≈ 0.71   | ≈ 0.70    | ≈ 0.95 | ≈ 0.75 |

**Interpretation.**  
The Random Forest consistently outperforms the linear benchmark, indicating the presence of **nonlinear interactions** in emissions dynamics.


⸻

4.5 Explainability with SHAP

Model predictions are interpreted using SHAP (SHapley Additive exPlanations) applied to the Random Forest.

SHAP values decompose each prediction into feature-level contributions to the probability of entering a low-emissions regime.

Outputs
	•	SHAP summary (dot) plot
	•	SHAP summary (bar) plot
	•	Dependence plot for the top-ranked feature

Across all visualizations, d_co2_per_capita emerges as the most influential predictor.

This confirms that recent emissions dynamics, rather than income or population levels, drive regime classification.

⸻

4.6 Q4A – Multicountry Robustness Extension

To assess external validity, the analysis is extended to a large multicountry panel covering:
	•	199 countries
	•	1990–2018
	•	6,488 country–year observations

Data sources combine:
	•	World Bank macroeconomic indicators
	•	OWID CO₂ emissions data

Updated class balance
	•	target = 1: 1,138 observations
	•	target = 0: 4,355 observations

This introduces realistic imbalance and heterogeneity absent from the baseline setup.

⸻

## Multicountry Classification Results

**Average performance across rolling temporal splits:**

| Model               | Accuracy | Precision | Recall | F1   |
|---------------------|----------|-----------|--------|------|
| Random Forest       | ≈ 0.74   | ≈ 0.42    | ≈ 0.34 | ≈ 0.35 |
| Logistic Regression | ≈ 0.77   | ≈ 0.48    | ≈ 0.01 | ≈ 0.02 |

While overall accuracy remains moderate, recall and F1 decline substantially, reflecting the intrinsic difficulty of predicting emissions regime shifts across heterogeneous national contexts.

Crucially, this drop in performance indicates that:
	•	Regime transitions are not mechanically determined by current emissions changes.
	•	Multicountry decarbonization dynamics exhibit structural uncertainty rather than deterministic rules.

⸻

4.7 Policy Interpretation

Three policy-relevant insights emerge:
	1.	Dynamics dominate levels
Changes in emissions growth carry more predictive power than GDP or population levels.
	2.	Regime shifts are probabilistic, not deterministic
Perfect classification in small samples disappears once realistic cross-country heterogeneity is introduced.
	3.	Early-warning rather than prediction
The model is best interpreted as a risk and prioritization tool, not a deterministic forecasting engine.

These findings reinforce Q3, where small differences in decoupling rates generated large long-run emissions gaps, but with substantial uncertainty around transition timing.

⸻

4.8 Limitations
	•	Target definition is reduced-form and outcome-based.
	•	Class imbalance complicates recall for rare transition events.
	•	SHAP explanations are descriptive rather than causal.

These limitations are structural rather than methodological and reflect real-world policy uncertainty.

⸻

4.9 Conclusion

Q4 demonstrates that emissions regime transitions can be identified using a small, interpretable set of macro-environmental indicators, but that predictive power declines sharply when moving from stylized to global settings.

Taken together, Q2–Q4 provide a coherent empirical narrative:

Economic growth alone does not determine emissions outcomes.
What matters is how emissions evolve relative to growth—and how uncertain those dynamics are across countries.

This directly motivates Q5, where classification outputs are used not for prediction, but for country prioritization under uncertainty.


