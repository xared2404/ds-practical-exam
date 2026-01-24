# Q3. Scenario Analysis and Projections

This section develops forward-looking CO₂ emissions projections for Mexico and the United States, building directly on the econometric models estimated in Q2. The objective is to assess how alternative assumptions regarding economic growth and decarbonization translate into divergent emissions trajectories over the period 2024–2035.

All projections rely on a balanced country–year panel covering 1990–2023 and are explicitly interpreted as **scenario-based projections**, not point forecasts.

---

## Q3.1 Baseline and Alternative Emissions Scenarios (2024–2035)

# Q3 — Scenario analysis and projections (2024–2035)

## 1. Objective

Project medium-term CO₂ emissions under alternative decarbonization assumptions. Scenarios are conditional projections (not forecasts) based on models estimated in Q2 and a balanced panel for 1990–2023.

---

## 2. Methods

- Functional form: log-link specifications for total and per-capita emissions to ensure positive predictions.
- Inputs: extrapolated GDP and population paths (recent historical growth rates) combined with estimated coefficients.
- Scenarios: Baseline, No-Decoupling, Strong Decoupling.

---

## 3. Scenario definitions

- Baseline: moderate ongoing decoupling (business-as-usual).
- No-Decoupling: time trend set to zero; emissions scale with GDP and population.
- Strong Decoupling: amplified negative time trend reflecting accelerated mitigation.

Reproducible figure script: `PYTHONPATH=src python scripts/q3_figures.py`

---

## 4. Key results

Total emissions (Figure 1):
- Baseline: gradual decline.
- No-Decoupling: sharp increases (upper bound).
- Strong Decoupling: substantial reductions.

Per-capita emissions (Figure 2):
- Decline in most scenarios except No-Decoupling.
- USA remains higher per-capita but gap narrows under strong decoupling.

Avoided emissions by 2035 (approx.):
- Mexico: Baseline vs No-Decoupling ≈ 190 Mt; Strong vs No-Decoupling ≈ 255 Mt.
- USA: Baseline vs No-Decoupling ≈ 2,500 Mt; Strong vs No-Decoupling ≈ 3,360 Mt.

---

## 5. Robustness and sensitivity

- Functional-form checks (linear vs log-link) preserve scenario ordering.
- Time-trend sensitivity shows small changes in decoupling compound into large cumulative differences.
- Country-specific checks: qualitative patterns stable despite small panel size.

---

## 6. Policy implications and limitations

- Policy implications: decarbonization dynamics (policy + technology) drive outcomes; early action yields large avoided emissions.
- Limitations: scenarios are conditional, panel limited to two countries, decoupling captured via reduced-form trends, and long-run GDP/population uncertainty not fully modeled.

---

## 7. Synthesis

Scenario analysis confirms that future emissions paths are sensitive to decarbonization trajectories, motivating regime detection (Q4) and policy-prioritization exercises (Q5).


---

### Q3.3.2 Limitations of the Scenario-Based Approach

Despite their usefulness, the projections presented in Q3 are subject to several important limitations.

First, the scenarios are **not forecasts** but conditional projections. They extrapolate historical relationships under stylized assumptions about future growth and decarbonization trends. Unexpected structural breaks—such as technological breakthroughs, geopolitical shocks, or major policy reversals—could lead to substantially different outcomes.

Second, the panel includes only two countries. While this allows for a transparent comparison, it limits the external validity of the results. The estimated time trends and income effects may not generalize to economies with different institutional structures, energy mixes, or development paths.

Third, the decoupling mechanisms are captured in reduced form through time trends rather than explicit policy variables. As a result, the analysis cannot identify which specific policies or technologies drive the observed decarbonization dynamics.

Finally, uncertainty around long-run GDP and population growth is not modeled explicitly. The scenarios condition on smooth extrapolations of recent trends, which may underestimate future volatility.

These limitations imply that the results should be interpreted as **illustrative and comparative**, rather than predictive.

---

### Q3.3.3 Integrated Synthesis

Taken together, Q3.1–Q3.3 provide a coherent picture of medium-term emissions dynamics.

The scenario analysis shows that future CO₂ emissions paths are highly sensitive to assumptions about decarbonization, while the robustness checks confirm that these conclusions are stable across alternative functional forms and parameter choices. Time-driven dynamics dominate income effects, and policy-relevant insights are not artifacts of a particular specification.

The key message is that **decarbonization is a choice, not an automatic outcome of growth**. Without sustained policy intervention, emissions would rise markedly; with accelerated decoupling, substantial reductions are achievable within little more than a decade.

From a methodological perspective, the exercise illustrates how econometric models estimated on historical data can be combined with transparent scenario assumptions to inform policy discussions—while also highlighting the importance of robustness analysis and cautious interpretation.

This completes the scenario-based assessment of emissions trajectories. The next section builds on these findings to draw broader conclusions about economic growth, environmental sustainability, and the role of policy in shaping long-run outcomes.

## Figures

Representative figures (stored in `data/processed/`):

- Baseline total CO₂ projections (2035, Mt):

	![Q3 baseline CO2 Mt 2035](../data/processed/q3_baseline_co2_mt_2035.png)

- Scenario comparisons (total CO₂, 2035, Mt):

	![Q3 scenarios CO2 Mt 2035](../data/processed/q3_scenarios_co2_mt_2035.png)

- Per-capita projections (example):

	![Q3 baseline CO2 per capita 2035](../data/processed/q3_baseline_co2_pc_2035.png)


These results motivate a shift from long-run scenario projection to regime detection. If small differences in decoupling rates generate large emissions gaps over time, an immediate policy-relevant question emerges: can countries that are already entering low-emissions regimes be identified early? This question is addressed in Q4.


While Q3 demonstrates that small differences in decoupling rates generate large long-run emissions gaps, it does not address whether countries already entering low-emissions regimes can be identified in real time. This motivates a shift from scenario projection to regime detection, developed in Q4.
