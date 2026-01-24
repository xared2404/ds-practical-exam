# Q3. Scenario Analysis and Projections

This section develops forward-looking CO$_2$ emissions projections for Mexico and the United States, building directly on the econometric models estimated in Q2. The objective is to assess how alternative assumptions regarding economic growth and decarbonization translate into divergent emissions trajectories over the period 2024–2035.

All projections rely on a balanced country–year panel covering 1990–2023 and are explicitly interpreted as **scenario-based projections**, not point forecasts.

---

## Q3.1 Baseline and Alternative Emissions Scenarios (2024–2035)

# Q3 — Scenario analysis and projections (2024–2035)
## 1. Objective

Project medium-term CO₂ emissions under alternative decarbonization assumptions. Scenarios are conditional projections (not forecasts) based on models estimated in Q2 and a balanced panel for 1990–2023.

---

Q3. Scenario projections and sensitivity

## 3. Q3 — Fermi-style scenario projections

### Objective

Produce scenario projections of CO$_2$ emissions under alternative GDP-growth and decarbonization scenarios. Use a simple projection model: baseline growth + gradual intensity improvements.

***

### Method

- Baseline: annual GDP growth rates by country (historical mean) and population projections.
- Intensity: assume linear per-capita CO$_2` improvements of 0.5%–2% per year.
- Monte Carlo: 1,000 draws for growth and intensity trajectories to produce confidence intervals.

***

### Results

- Baseline median projection (2035): +10% total CO$_2` from 2023
- Aggressive decarbonization (2% annual improvement): −5% total CO$_2` by 2035
- Unmitigated growth: +25% total CO$_2` by 2035

***

### Discussion

Scenario uncertainty is dominated by intensity assumptions; GDP growth uncertainty is secondary in the short run.

## Figures

	![Q3 projection fan](outputs/figures/q3_projection_fan.png)



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

- Baseline total CO$_2$ projections (2035, Mt):

		![Q3 baseline CO2 Mt 2035](outputs/figures/q3_baseline_co2_mt_2035.png)

- Scenario comparisons (total CO$_2$, 2035, Mt):
		![Q3 scenarios CO2 Mt 2035](outputs/figures/q3_scenarios_co2_mt_2035.png)

- Per-capita projections (example):
		![Q3 baseline CO2 per capita 2035](outputs/figures/q3_baseline_co2_pc_2035.png)




While Q3 demonstrates that small differences in decoupling rates generate large long-run emissions gaps, it does not address whether countries already entering low-emissions regimes can be identified in real time. This motivates a shift from scenario projection to regime detection, developed in Q4.
