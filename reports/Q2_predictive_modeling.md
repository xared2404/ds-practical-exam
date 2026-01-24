Q2. Economic Activity, Emissions, and Decoupling Dynamics

(Mexico and the United States, 1990–2023)

Q2.1 Objective and Research Question

This section examines the relationship between economic activity and CO₂ emissions in Mexico and the United States over the period 1990–2023.

The central research question is:

How are CO₂ emissions related to economic growth and population size, and is there evidence of structural decoupling over time?

The analysis serves three purposes:
	1.	Establish baseline scale and intensity effects between GDP and emissions.
	2.	Identify the role of time-driven dynamics consistent with decarbonization.
	3.	Provide empirical foundations for the scenario analysis (Q3) and regime classification (Q4).

⸻

Q2.2 Data and Econometric Framework

A balanced country–year panel is constructed for Mexico and the United States covering 1990–2023 (68 observations).

All models are estimated using Ordinary Least Squares (OLS) with heteroskedasticity-robust (HC3) standard errors.

Two core specifications are considered:
	•	Model A: Total CO₂ emissions (scale effects)
	•	Model B: CO₂ emissions per capita (intensity effects)

Additional robustness specifications include country fixed effects and Environmental Kuznets Curve (EKC) tests.

⸻

Q2.3 Model A: Total CO₂ Emissions (Scale Effects)

Specification

\text{CO₂}{it} = \beta_0 + \beta_1 \ln(\text{GDP}{it}) + \beta_2 \ln(\text{Population}_{it}) + \beta_3 \text{Year}_t + \beta_4 \text{USA}i + \varepsilon{it}

Key Results
	•	GDP (log): Positive and highly significant
→ Economic scale is the dominant driver of total emissions.
	•	Population (log): Not statistically significant
→ Population adds little explanatory power once GDP is controlled for.
	•	Time trend: Negative and highly significant
→ Indicates gradual decoupling over time.
	•	Country dummy (USA): Not significant
→ No structural difference after controlling for scale and time.

Model fit: R² ≈ 0.99

Interpretation

Total emissions are primarily explained by economic scale. However, the negative time trend reveals that emissions grow more slowly than GDP, signaling partial decoupling driven by technological change, energy efficiency, or structural shifts.

⸻

Q2.4 Model B: CO₂ Emissions per Capita (Intensity Effects)

Motivation

Total emissions are mechanically dominated by economic size. To isolate environmental intensity and enable meaningful cross-country comparison, emissions are normalized by population.

Specification

\text{CO₂pc}{it} = \alpha_0 + \alpha_1 \ln(\text{GDP}{it}) + \alpha_2 \text{Year}_t + \alpha_3 \text{USA}i + u{it}

Key Results
	•	GDP (log): Positive and statistically significant
→ Higher income is associated with higher per-capita emissions.
	•	Time trend: Negative and highly significant
→ Strong evidence of declining emissions intensity over time.
	•	USA dummy: Negative and significant
→ Conditional on income and time, the United States exhibits lower per-capita emissions than Mexico.

Model fit: R² ≈ 0.99

Interpretation

While economic growth remains carbon-intensive at the per-capita level, emissions intensity declines systematically over time. This suggests that decarbonization operates primarily through dynamic mechanisms, not income-driven thresholds.

⸻

Q2.5 Fixed Effects and EKC Robustness

Country and Year Fixed Effects

Introducing country and year fixed effects substantially weakens the GDP–emissions relationship. Once structural heterogeneity and global time shocks are absorbed, income effects lose statistical significance.

This indicates that pooled GDP–emissions correlations are largely driven by:
	•	long-run trends, and
	•	cross-country structural differences.

Environmental Kuznets Curve (EKC)

Quadratic income specifications do not support the EKC hypothesis:
	•	Income terms are not statistically significant under fixed effects.
	•	Estimated signs do not exhibit the inverted-U pattern.

Conclusion:
There is no evidence that emissions decline automatically beyond an income threshold.

⸻

Q2.6 Synthesis and Link to Subsequent Sections

Three core findings emerge:
	1.	Economic scale matters for emissions levels, but not deterministically.
	2.	Time dynamics dominate income effects, indicating decoupling driven by technology and policy rather than growth alone.
	3.	No evidence supports an Environmental Kuznets Curve once structural and temporal confounders are controlled for.

These results directly motivate:
	•	Q3, where emissions trajectories are simulated under alternative decoupling assumptions.
	•	Q4, where short-run emissions dynamics are used to classify regime transitions.
	•	Q5, where investment prioritization leverages dynamic rather than static indicators.

⸻

Q2.7 Conclusion

Q2 demonstrates that emissions outcomes are not mechanically tied to economic growth. While GDP explains emissions scale, sustained reductions arise from dynamic, time-dependent processes rather than income levels.

This insight anchors the broader empirical narrative of the exam:

Growth does not guarantee decarbonization—policy, technology, and timing do.
