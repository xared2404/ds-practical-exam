Q4. Classification, Explainability, and Policy Implications

4.1 Objective and Conceptual Framing

This section develops a supervised classification framework to identify emissions regime transitions across countries. The objective is not to forecast future emissions levels, but to detect structural changes in emissions dynamics that signal a country’s emerging capacity to decouple emissions from economic activity.

Q4 complements the previous sections in a progressive analytical sequence:
	•	Q2 established that temporal dynamics dominate static income effects in explaining emissions outcomes.
	•	Q3 demonstrated that long-run emissions trajectories are highly sensitive to small differences in decoupling rates.
	•	Q4 shifts the focus from projection to pattern recognition, asking whether countries that enter low-emissions-growth regimes share identifiable and interpretable characteristics.

Rather than asking how much emissions will change, Q4 addresses a policy-relevant diagnostic question:

Which observable macro-environmental dynamics distinguish countries that begin reducing emissions, and how early can such transitions be detected?

This reframing is motivated by policy timing: early identification of regime shifts enables more timely and better-targeted intervention.

⸻

4.2 Target Variable Definition

Regime-Based Classification

The classification task is defined at the country–year level. The binary target variable captures whether a country enters a low-emissions-growth regime in a given year:
	•	target = 1: Per-capita CO₂ emissions decline relative to the previous year
	•	target = 0: Per-capita CO₂ emissions are flat or increasing

This reduced-form definition treats observed emissions dynamics as a proxy for a broader set of underlying mechanisms, including:
	•	energy-system transitions,
	•	regulatory tightening,
	•	technological change, and
	•	institutional capacity for sustained decarbonization.

Crucially, the target does not represent a policy variable and should not be interpreted causally. Its purpose is to identify incipient regime transitions, not to attribute outcomes to specific instruments or reforms.

⸻

4.3 Multi-Country Panel Construction (Q4A)

Motivation

An initial two-country setup (Mexico and the United States) was informative for conceptual validation but limited in external validity. To address this constraint, Q4 is extended into a large-scale multicountry robustness exercise (Q4A).

Data Sources
	•	World Bank: GDP (current USD), population
	•	Our World in Data (OWID): CO₂ emissions (total and per capita)

Panel Characteristics
	•	Countries: ~200 non-aggregate economies
	•	Years: 1990–2023
	•	Final usable sample (after feature construction and lagging):
approximately 5,500 country–year observations
	•	Output: data/processed/q4a_multicountry_panel.parquet

The resulting panel preserves both cross-sectional heterogeneity and temporal ordering, strengthening generalizability and enabling rigorous time-aware validation.

⸻

4.4 Feature Engineering

The feature set is deliberately compact, interpretable, and theory-consistent, closely mirroring the mechanisms emphasized in Q2 and Q3.

Feature Categories

Economic and Demographic Levels
	•	ln_gdp
	•	ln_population
	•	ln_gdp_pc

Emissions and Intensity Levels
	•	co2_per_capita
	•	ln_co2_intensity

Dynamic Indicators (First Differences)
	•	d_ln_gdp_pc
	•	d_co2_per_capita
	•	d_ln_co2_intensity

Time Control
	•	year_norm (normalized year index)

Dynamic variables play a central role. Consistent with Q2 and Q3, changes over time dominate static levels in explaining regime transitions, reinforcing the importance of emissions trajectories rather than economic scale alone.

Output: data/processed/q4a_features.parquet

⸻

4.5 Classification Models and Validation Strategy

Two supervised learning models are estimated:
	1.	Logistic Regression
A standardized linear benchmark designed to capture average marginal effects.
	2.	Random Forest Classifier
A depth-limited, class-weighted ensemble model capable of capturing nonlinear interactions and threshold effects in emissions dynamics.

Temporal Validation (Rolling Splits)

To avoid information leakage and respect the time structure of the data, evaluation uses a rolling temporal validation strategy:
	•	Minimum training window: 10 years
	•	Fixed test window: 5 years
	•	Multiple rolling cutoffs evaluated sequentially

Each test set contains only observations occurring strictly after the corresponding training period.

## Average Performance Across Rolling Splits (Q4A)

| Model               | Accuracy | Precision | Recall | F1   |
|---------------------|----------|-----------|--------|------|
| Random Forest       | ≈ 0.74   | ≈ 0.42    | ≈ 0.34 | ≈ 0.35 |
| Logistic Regression | ≈ 0.77   | ≈ 0.48    | ≈ 0.01 | ≈ 0.02 |

The Random Forest substantially outperforms the linear benchmark in recall and F1, indicating the presence of nonlinear and interaction-driven structure in emissions dynamics. The lower overall performance relative to the small-sample baseline reflects the increased difficulty of the multicountry task and confirms that regime detection is not driven by trivial decision rules.

⸻

4.6 Explainability and Diagnostic Analysis

To interpret model predictions, SHAP (SHapley Additive exPlanations) is applied to the trained Random Forest model.

SHAP values quantify each feature’s marginal contribution to the predicted probability of entering a low-emissions-growth regime.

Key Findings
	•	Dynamic emissions variables dominate feature-importance rankings
	•	Level variables (GDP, population) play a secondary role
	•	The sign and magnitude of SHAP values vary across countries and periods, reflecting heterogeneous and path-dependent transition dynamics

Diagnostic checks confirm that the target is not mechanically encoded by any single feature once lag structures and multicountry variation are introduced. This supports interpreting the classifier as detecting genuine regime patterns rather than construction artifacts.

⸻

4.7 Policy Interpretation

Three policy-relevant insights emerge:
	1.	Dynamics dominate levels
Short-run changes in emissions and intensity carry more predictive power than income or population levels.
	2.	Regime shifts reflect decoupling capacity
Countries are classified as successful not because they are rich or small, but because their emissions trajectories change direction.
	3.	Early-warning signals for policy
Monitoring emissions growth rates provides earlier and more informative signals of structural transition than level-based indicators.

These findings reinforce the scenario analysis in Q3, where small differences in decoupling rates generated large long-run emissions gaps.

⸻

4.8 Limitations

Several limitations apply:
	•	The regime definition is reduced-form and not policy-instrument specific.
	•	Classification results reflect correlation, not causation.
	•	Despite the multicountry expansion, data availability remains uneven across regions.

Nevertheless, the consistency of results across econometric (Q2), scenario-based (Q3), and machine-learning (Q4) approaches supports the robustness of the core conclusions.

⸻

4.9 Conclusion

Q4 demonstrates that emissions regime transitions can be detected using a small, interpretable set of macro-environmental indicators when temporal structure is properly respected. Dynamic emissions measures consistently outperform static economic variables, and explainability analysis confirms their central role.

Taken together, Q2–Q4 provide a coherent empirical narrative:

Economic growth alone does not determine emissions outcomes.
What matters is how emissions evolve relative to growth—and how quickly those dynamics change.

This insight motivates the final step of the analysis: translating regime detection into strategic investment and policy prioritization, developed in Q5.

While Q4 identifies which countries are statistically more likely to enter low-emissions regimes, it does not address how limited financial and policy resources should be allocated across countries. Translating regime detection into strategic prioritization is the focus of Q5.

