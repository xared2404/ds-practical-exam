Q2. Predictive Modeling of CO₂ Emissions

2.1 Research Question and Hypotheses

# Q2 — Predictive modeling of CO₂ emissions

## 1. Objective

This section evaluates how CO₂ emissions relate to economic activity and population size in Mexico and the United States for 1990–2023. It distinguishes scale effects (total emissions) from intensity effects (per-capita emissions) and tests whether temporal dynamics dominate static income relationships.

---

## 2. Models and hypotheses

Model A (Total CO₂ emissions)
- Dependent: `co2_mt` (total CO₂ emissions, Mt)
- Explanatory: `gdp_current_usd`, `population`, `year`, `country`

Hypotheses:
- H1: Higher GDP → higher total CO₂ (β1 > 0)
- H2: Larger population → higher total CO₂ (β2 > 0)
- H3: Statistically significant time trend exists (β3 ≠ 0)
- H4: Structural country differences may be present (β4 ≠ 0)

Model B (CO₂ per capita)
- Dependent: `co2_per_capita` (tons/person)
- Explanatory: `gdp_per_capita`, `year`, `country`

Rationale: population is excluded from Model B because it is implicit in the per-capita outcome.

---

## 3. Estimation and diagnostics

- Estimation method: OLS on a balanced panel (Mexico, USA; 1990–2023) with heteroskedasticity-robust (HC3) standard errors.
- Additional checks: fixed-effects specifications and quadratic (EKC) income tests.

Key diagnostics indicate strong explanatory power for scale-based models but presence of serial correlation and multicollinearity typical of short panels.

---

## 4. Main results

Model A (total emissions):
- Observations: 68
- R² ≈ 0.99 — scale and time effects explain most variation.
- Interpretation: GDP has a positive and significant association with total CO₂; the estimated year trend is negative, suggesting partial decoupling over time.

Model B (per-capita):
- Observations: 68
- R² ≈ 0.99
- Interpretation: GDP per capita positively correlates with per-capita emissions, but a significant negative time trend indicates improving emissions intensity over time.

Fixed-effects and EKC tests reduce the apparent income effect, pointing to the importance of time and structural factors.

---

## 5. Synthesis

1. Economic scale explains levels but not dynamics.
2. Time effects dominate income effects for changes in emissions.
3. Structural decoupling is not automatic; policy and technology matter.

The econometric findings motivate scenario-based projections in Q3.
Estimation Results (Model A)

	•	Observations: 68

