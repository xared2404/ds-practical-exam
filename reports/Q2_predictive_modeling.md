Q2. Predictive Modeling of CO₂ Emissions

2.1 Research Question and Hypotheses

Research Question

How are CO₂ emissions related to economic activity and population size in Mexico and the United States between 1990 and 2023?

This section evaluates whether economic growth and demographic scale are sufficient to explain emissions dynamics, or whether temporal and structural factors dominate.

⸻

Model A: Total CO₂ Emissions

Dependent variable
	•	co2_mt: Total CO₂ emissions (million tonnes)

Independent variables
	•	gdp_current_usd: Gross Domestic Product (current USD)
	•	population: Total population
	•	year: Linear time trend
	•	country: Country indicator (USA vs. Mexico)

Hypotheses
	•	H1: Higher GDP is associated with higher total CO₂ emissions (β₁ > 0)
	•	H2: Larger population leads to higher total CO₂ emissions (β₂ > 0)
	•	H3: There is a statistically significant time trend in emissions (β₃ ≠ 0)
	•	H4: Structural differences exist between Mexico and the United States (β₄ ≠ 0)

⸻

Model B: CO₂ Emissions per Capita

Dependent variable
	•	co2_per_capita: CO₂ emissions per person (metric tons)

Independent variables
	•	gdp_per_capita: GDP per capita
	•	year: Linear time trend
	•	country: Country indicator

Hypotheses
	•	H1b: Higher GDP per capita is associated with higher CO₂ emissions per capita (β₁ > 0)
	•	H2b: CO₂ emissions per capita change systematically over time, reflecting structural or technological shifts

⸻

Transition to estimation

These hypotheses are evaluated using panel regressions that explicitly distinguish scale effects from intensity effects, allowing emissions dynamics to be decomposed into economic, demographic, and temporal components.

⸻

2.2 Econometric Analysis: OLS Models

Model A Specification: Total Emissions

An Ordinary Least Squares (OLS) model is estimated using a balanced panel of Mexico and the United States for the period 1990–2023:

\text{CO₂}{it} = \beta_0 + \beta_1 \ln(\text{GDP}{it}) + \beta_2 \ln(\text{Population}_{it}) + \beta_3 \text{Year}_t + \beta_4 \text{USA}i + \varepsilon{it}

Heteroskedasticity-robust (HC3) standard errors are reported.

⸻

Estimation Results (Model A)
	•	Observations: 68
	•	R²: 0.994
	•	Adjusted R²: 0.994

The model explains nearly all variation in total CO₂ emissions, reflecting strong scale and time effects.

⸻

Interpretation

Economic scale (ln GDP)
The GDP coefficient is positive and statistically significant (p < 0.001). A 1% increase in GDP is associated with a substantial increase in total CO₂ emissions, supporting H1.

Population (ln Population)
The population coefficient is negative and statistically insignificant. Once GDP and time trends are controlled for, population size adds little explanatory power, leading to rejection of H2 in this specification.

Time trend (Year)
The coefficient on year is negative and highly significant (p < 0.001), indicating a gradual decline in emissions over time after controlling for scale. This supports H3 and suggests partial decoupling driven by technological or structural change.

Country effect (USA dummy)
The country dummy is not statistically significant, indicating no structural difference between Mexico and the United States once GDP, population, and time are accounted for. H4 is not supported.

⸻

Diagnostics

Serial correlation and multicollinearity are present, as expected in short panel time-series data. While these features affect coefficient precision, they do not undermine the qualitative conclusions regarding scale and time effects.

⸻

Bridge to Model B

Because total emissions are mechanically dominated by economic scale, this specification provides limited insight into emissions efficiency or structural decarbonization. To address this limitation, an alternative per-capita specification is estimated.

⸻

2.3 Alternative Specification: CO₂ Emissions per Capita

Model B Specification

\text{CO₂pc}{it} = \alpha_0 + \alpha_1 \ln(\text{GDP}{it}) + \alpha_2 \text{Year}_t + \alpha_3 \text{USA}i + u{it}

Population is excluded, as it is embedded in the dependent variable.

⸻

Estimation Results (Model B)
	•	Observations: 68
	•	R²: 0.989
	•	Robust covariance: HC3

All explanatory variables are statistically significant at the 1% level.

⸻

Interpretation

Income effect
Higher GDP is associated with higher emissions per capita, indicating that economic growth remains carbon-intensive in per-person terms.

Time trend
The negative and significant time coefficient indicates a structural decline in emissions intensity over time, consistent with gradual decarbonization.

Country effect
Conditional on GDP and time, the United States exhibits lower per-capita emissions than Mexico, reflecting structural and technological differences.

⸻

2.4 Fixed Effects and EKC Extensions

Fixed Effects Benchmark

Introducing country and year fixed effects substantially weakens the GDP–emissions relationship, indicating that much of the correlation observed in pooled models is driven by long-run trends and cross-country differences rather than within-country variation.

Environmental Kuznets Curve (EKC) Test

Quadratic income specifications do not support the EKC hypothesis. Income terms are statistically insignificant once fixed effects are introduced, and estimated signs do not correspond to an inverted-U relationship.

⸻

2.5 Synthesis and Transition to Q3

The econometric evidence yields three central conclusions:
	1.	Economic scale explains emissions levels, but not emissions dynamics.
	2.	Time effects dominate income effects in explaining changes in emissions.
	3.	Structural decoupling is not automatic and cannot be inferred from income alone.

These findings motivate a shift away from static regression analysis toward dynamic scenario exploration.
In the next section (Q3), emissions trajectories are simulated under alternative decoupling assumptions to assess how small changes in dynamics translate into large long-run outcomes.


