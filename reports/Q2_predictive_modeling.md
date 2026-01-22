1. Research Question and Hypotheses

Research question:
How are CO₂ emissions related to economic activity and population size in Mexico and the United States between 1990 and 2023?

⸻

Model A: Total CO₂ emissions
    •    Dependent variable (DV):
co2_mt – Total CO₂ emissions (million tonnes)
    •    Independent variables (IVs):
    •    gdp_current_usd – GDP (current USD)
    •    population – Total population
    •    year – Time trend
    •    country – Country fixed effect (USA vs Mexico)

Hypotheses:
    •    H1: Higher GDP is associated with higher total CO₂ emissions
(β₁ > 0)
    •    H2: Larger population leads to higher total CO₂ emissions
(β₂ > 0)
    •    H3: There is a statistically significant time trend in emissions
(β₃ ≠ 0)
    •    H4: There are structural differences in emissions between Mexico and the United States
(β₄ ≠ 0)

⸻

Model B: CO₂ emissions per capita
    •    Dependent variable (DV):
co2_per_capita – CO₂ emissions per person (tons)
    •    Independent variables (IVs):
    •    gdp_per_capita – GDP per capita
    •    year – Time trend
    •    country – Country fixed effect

Hypotheses:
    •    H1b: Higher GDP per capita is associated with higher CO₂ emissions per capita
(β₁ > 0)
    •    H2b: CO₂ emissions per capita change systematically over time, reflecting structural or technological shifts.


2. Econometric Analysis: OLS Model and Hypothesis Testing


Model specification

To analyze the relationship between economic activity, population, and CO₂ emissions, an Ordinary Least Squares (OLS) model was estimated using a balanced panel of Mexico and the United States for the period 1990–2023.

The estimated model is:

\text{CO₂}{it} = \beta_0 + \beta_1 \ln(\text{GDP}{it}) + \beta_2 \ln(\text{Population}_{it}) + \beta_3 \text{Year}_t + \beta_4 \text{USA}i + \varepsilon{it}

where:
    •    \text{CO₂}_{it} is total CO₂ emissions (million tons),
    •    \ln(\text{GDP}_{it}) is the natural logarithm of GDP (current USD),
    •    \ln(\text{Population}_{it}) is the natural logarithm of population,
    •    \text{Year}_t captures common time trends,
    •    \text{USA}_i is a country dummy (1 = USA, 0 = Mexico).

Heteroskedasticity-robust (HC3) standard errors were used.

⸻

Hypotheses
    •    H1: Higher economic activity (GDP) is associated with higher CO₂ emissions.
    •    H2: Population size has a positive and significant effect on CO₂ emissions.
    •    H3: There exists a significant time trend in CO₂ emissions.
    •    H4: There are structural differences in emissions between Mexico and the United States after controlling for scale.

⸻

Estimation results summary
    •    Observations: 68
    •    R²: 0.994
    •    Adjusted R²: 0.994

The model explains nearly all the variation in total CO₂ emissions, which is expected given strong scale and time effects.

⸻

Interpretation of coefficients

GDP (ln)

The coefficient on ln(GDP) is positive and statistically significant (p < 0.001). A 1% increase in GDP is associated with an increase of approximately 38 million tons of CO₂, holding other variables constant.

This provides strong support for H1, confirming that economic growth is a major driver of total emissions.

⸻

Population (ln)

The coefficient on ln(Population) is negative and not statistically significant. Once GDP and time trends are controlled for, population size does not have an independent effect on total CO₂ emissions.

This result suggests strong multicollinearity between GDP and population and leads to the rejection of H2 in this specification.

⸻

Time trend (Year)

The year coefficient is negative and statistically significant (p < 0.001). After controlling for GDP, population, and country, total CO₂ emissions decline by approximately 65 million tons per year.

This indicates the presence of long-term decoupling forces such as technological improvements, energy efficiency gains, or structural economic changes, supporting H3.

⸻

Country dummy (USA)

The USA dummy is not statistically significant. After accounting for GDP, population, and time trends, there is no evidence of a structural difference in total CO₂ emissions between the United States and Mexico.

Therefore, H4 is not supported in this model.

⸻

Diagnostic discussion

The Durbin–Watson statistic indicates positive serial correlation, which is expected in panel time-series data. The high condition number suggests multicollinearity, mainly between GDP, population, and time. While this affects coefficient precision, it does not invalidate the overall findings.

⸻

Conclusion

The results indicate that:
    1.    Economic scale (GDP) is the primary determinant of total CO₂ emissions.
    2.    Population does not add explanatory power once GDP is included.
    3.    A significant negative time trend suggests partial decoupling of emissions from economic growth.
    4.    Cross-country differences disappear after controlling for scale.

These findings motivate an alternative specification using per-capita emissions, which is explored in the next section.


Alternative specification: CO₂ per capita (Model B)

Motivation

The baseline model explains total CO₂ emissions primarily through economic scale (GDP), which mechanically dominates population and country effects. To address this limitation and analyze environmental intensity rather than size, an alternative specification using CO₂ emissions per capita is estimated.

This transformation allows for a more meaningful cross-country comparison and reduces multicollinearity between GDP and population.

⸻

Model specification

The alternative model is specified as:

\text{CO₂pc}{it} = \alpha_0 + \alpha_1 \ln(\text{GDP}{it}) + \alpha_2 \text{Year}_t + \alpha_3 \text{USA}i + u{it}

where:
    •    \text{CO₂pc}_{it} is CO₂ emissions per capita (tons per person),
    •    \ln(\text{GDP}_{it}) captures income effects,
    •    \text{Year}_t captures common time trends,
    •    \text{USA}_i captures structural differences in emissions intensity.

Population is excluded since it is already incorporated into the dependent variable.

⸻

Hypotheses (Model B)
    •    H5: Higher income levels are associated with higher CO₂ emissions per capita.
    •    H6: There is a significant time trend in per-capita emissions.
    •    H7: The United States exhibits higher CO₂ emissions per capita than Mexico, controlling for income and time.

⸻

Expected interpretation framework
    •    A positive \alpha_1 would indicate that economic growth remains carbon-intensive even after adjusting for population.
    •    A negative \alpha_2 would suggest decoupling at the per-capita level, consistent with cleaner technologies or energy transitions.
    •    A positive and significant \alpha_3 would confirm persistent structural differences between the United States and Mexico in emissions intensity.

⸻

Link to empirical patterns

Descriptive analysis and the GDP–CO₂ per capita scatter plot show:
    •    A clear separation between the United States and Mexico.
    •    A downward trend in per-capita emissions in the United States after 2007.
    •    A flatter and lower emissions trajectory for Mexico.

These patterns motivate the per-capita regression and provide strong priors for H7.

⸻

Transition

The results of Model B allow us to distinguish scale effects from intensity effects, setting the foundation for:
    •    robustness checks,
    •    environmental Kuznets–type interpretations,
    •    or scenario-based projections in the next section.


Econometric Analysis (OLS Models)


Model B: Determinants of CO₂ Emissions per Capita (1990–2023)

Model specification

We estimate the following Ordinary Least Squares (OLS) model with heteroskedasticity-robust (HC3) standard errors:

\text{CO₂ per capita}_{it} = \beta_0
    •    \beta_1 \ln(\text{GDP}_{it})
    •    \beta_2 \text{Year}_t
    •    \beta_3 \text{USA}_i
    •    \varepsilon_{it}

Where:
    •    CO₂ per capita is measured in metric tons per person
    •    GDP corresponds to GDP in current USD (log-transformed)
    •    Year captures the global time trend
    •    USA is a dummy variable equal to 1 for the United States and 0 for Mexico
    •    The sample includes Mexico and the United States for the period 1990–2023

⸻

Estimation results (Model B)
    •    Number of observations: 68
    •    R²: 0.989
    •    Robust covariance: HC3

All explanatory variables are statistically significant at the 1% level.

⸻

Interpretation of coefficients

1. Economic scale effect (ln GDP)
The coefficient on log GDP is positive and statistically significant:
    •    β₁ ≈ 16.42 (p < 0.001)

This indicates that economic growth is strongly associated with higher CO₂ emissions per capita. Holding other factors constant, increases in GDP are linked to higher individual carbon intensity, consistent with scale effects dominating efficiency gains during the observed period.

⸻

2. Time trend (Year)
The coefficient on Year is negative and highly significant:
    •    β₂ ≈ −0.53 (p < 0.001)

This suggests a structural decline in CO₂ emissions per capita over time, after controlling for GDP and country effects. This pattern is consistent with technological improvements, energy efficiency gains, and environmental regulation becoming more effective over time.

⸻

3. Country effect (USA dummy)
The USA dummy has a large and negative coefficient:
    •    β₃ ≈ −23.05 (p < 0.001)

Conditional on GDP and time, the United States exhibits lower CO₂ emissions per capita than Mexico within this specification. This result reflects differences in economic structure, energy composition, and efficiency that are not fully captured by GDP alone.

⸻

Model diagnostics and caveats
    •    The very high R² (0.989) indicates that GDP, time, and country effects explain nearly all the variation in CO₂ per capita within this two-country panel.
    •    The Durbin–Watson statistic (~0.50) suggests potential serial correlation, which is expected in time-series cross-sectional data.
    •    The large condition number indicates possible multicollinearity between GDP and time trends; therefore, coefficient magnitudes should be interpreted cautiously, while signs and significance remain robust.

⸻

Key conclusions (Model B)
    1.    Economic growth is strongly associated with higher CO₂ emissions per capita.
    2.    There is a clear downward time trend in per-capita emissions, consistent with gradual decarbonization.
    3.    Significant cross-country differences remain even after controlling for GDP and time.
    4.    The results support the hypothesis that economic scale effects dominate, but technological and structural changes mitigate emissions over time.

⸻



We estimate two Ordinary Least Squares (OLS) models using a balanced country–year panel for Mexico and the United States covering the period 1990–2023. All models are estimated with heteroskedasticity-robust (HC3) standard errors.

Model A: Total CO₂ Emissions
Dependent variable:
    •    Total CO₂ emissions (million tons)

Explanatory variables:
    •    Log GDP (current USD)
    •    Log population
    •    Linear time trend
    •    Country dummy (USA = 1)

The results show a strong and statistically significant positive relationship between economic output and total CO₂ emissions. Higher GDP levels are associated with increased emissions, consistent with scale effects in production. The population coefficient is negative but not statistically significant, suggesting that once GDP is controlled for, population size does not independently drive total emissions.

The negative and significant time trend indicates a gradual decline in emissions over time after controlling for economic scale, possibly reflecting technological improvements, energy efficiency gains, or structural changes in the economy.

The country dummy for the United States is not statistically significant, implying that conditional on GDP, population, and time, emissions levels are not systematically different between Mexico and the United States.

The model exhibits an excellent fit (R² ≈ 0.99).

⸻

Model B: CO₂ Emissions per Capita
Dependent variable:
    •    CO₂ emissions per capita (metric tons)

Explanatory variables:
    •    Log GDP (current USD)
    •    Linear time trend
    •    Country dummy (USA = 1)

Results indicate a positive and statistically significant association between GDP and CO₂ emissions per capita, suggesting that higher income levels are linked to greater per-person carbon intensity. However, the negative and significant time trend implies that emissions per capita have declined over time, holding GDP constant.

The country dummy is negative and highly significant, indicating that, after controlling for income and time effects, the United States exhibits lower CO₂ emissions per capita relative to Mexico in the later period, reflecting stronger decarbonization trends.

This model also achieves a very high explanatory power (R² ≈ 0.99).

⸻

Comparison and Interpretation

Comparing both models highlights an important distinction between scale and intensity effects. While economic growth increases total emissions (Model A), emissions per capita exhibit a declining trend over time (Model B), suggesting partial decoupling between economic growth and environmental impact.

These findings are consistent with the environmental economics literature, particularly the role of technological change and efficiency improvements in reducing emissions intensity despite continued economic expansion.


### Model C: Country Fixed Effects


Model C introduces country fixed effects to control for time-invariant structural differences between Mexico and the United States. Given that the panel includes only two countries, the fixed-effects specification is equivalent to including a binary dummy variable for the United States.

As expected, the estimated coefficients and overall fit are numerically identical to Model A. This result reflects the fact that all cross-country heterogeneity is captured by a single indicator variable, and no additional within-country variation is absorbed by the fixed-effects transformation.

This equivalence provides a useful robustness check and confirms that the results are not driven by omitted country-level heterogeneity.


### Model D: Environmental Kuznets Curve (EKC)


Model D extends the baseline specification by introducing a quadratic term in log GDP in order to test the Environmental Kuznets Curve (EKC) hypothesis, which posits a non-linear (inverted U-shaped) relationship between economic development and environmental degradation.

The estimated model includes log GDP, squared log GDP, a linear time trend, and a country fixed effect for the United States. Heteroskedasticity-robust (HC3) standard errors are reported.

The results do not provide empirical support for the EKC hypothesis in this sample. While the squared income term is positive and the linear income term is negative, neither coefficient is statistically significant at conventional levels. This sign pattern corresponds to a U-shaped relationship rather than the expected inverted U-shape, and the lack of statistical significance prevents meaningful inference regarding a turning point.

In contrast, the time trend remains negative and statistically significant, indicating a systematic decline in CO₂ emissions over time after controlling for income levels. This suggests that temporal factors such as technological change, energy efficiency improvements, or environmental regulation may play a more important role than income-driven dynamics in explaining emissions trends.

The United States dummy remains negative and marginally significant, reflecting lower emissions levels relative to Mexico after controlling for income and time effects.

Overall, Model D improves slightly upon previous specifications in terms of information criteria (AIC/BIC), but does not support the existence of an Environmental Kuznets Curve for CO₂ emissions in this two-country panel.


## Regression Results Summary (Q2)

The table below summarizes the main regression results across four model specifications. All models are estimated using Ordinary Least Squares (OLS) with heteroskedasticity-robust (HC3) standard errors.

- Model A estimates total CO₂ emissions.
- Model B focuses on CO₂ emissions per capita.
- Model C introduces country fixed effects.
- Model D tests the Environmental Kuznets Curve (EKC) hypothesis by including a quadratic income term.

| Variable            | Model A: CO₂ (total) | Model B: CO₂ per capita | Model C: Fixed Effects | Model D: EKC |
|---------------------|---------------------|--------------------------|------------------------|--------------|
| Constant            | +***                | +***                     | +***                   | +**          |
| ln(GDP)             | +***                | +***                     | +***                   | −            |
| ln(GDP)²            | —                   | —                        | —                      | +            |
| ln(Population)      | −                   | —                        | −                      | —            |
| Year (trend)        | −***                | −***                     | −***                   | −***         |
| USA dummy            | −                   | −***                     | −                      | −*           |
| R²                  | 0.994               | 0.989                    | 0.994                  | 0.994        |
| N                   | 68                  | 68                       | 68                     | 68           |

Notes:  
Significance levels: * p < 0.10, ** p < 0.05, *** p < 0.01.  
All models report heteroskedasticity-robust (HC3) standard errors.


## Conclusion


This analysis examined the relationship between economic development and CO₂ emissions in Mexico and the United States over the period 1990–2023 using a panel data approach.

The results consistently show a strong association between economic scale and emissions, particularly when emissions are measured in absolute terms. Population size and income levels explain a large fraction of total emissions, while emissions per capita are more closely linked to income intensity and structural factors.

Across all specifications, the time trend is negative and statistically significant, indicating a gradual decoupling of economic activity from CO₂ emissions. This finding suggests that technological progress, energy efficiency improvements, and environmental policies have played a crucial role in reducing emissions intensity over time.

The inclusion of country fixed effects reveals systematic differences between Mexico and the United States, with the latter exhibiting lower emissions levels once income and time effects are controlled for. This highlights the importance of institutional and structural heterogeneity across countries.

Finally, the Environmental Kuznets Curve hypothesis is not supported by the data. The estimated income-emissions relationship does not display the expected inverted U-shape, and the income terms are not statistically significant once time effects are accounted for.

Overall, the evidence suggests that temporal dynamics and policy-driven factors are more relevant than income-driven nonlinearities in explaining long-run CO₂ emissions patterns in this two-country panel.


### Model C: Two-Way Fixed Effects (Country and Year)


To control for unobserved heterogeneity across countries and global shocks over time, a two-way fixed effects model was estimated including country and year fixed effects.

The results indicate that, once structural country differences and common time shocks are accounted for, GDP and population no longer exhibit statistically significant effects on total CO₂ emissions. This suggests that the strong correlation observed in pooled OLS models is largely driven by long-run trends and cross-country differences rather than within-country variation over time.

The very high R² is expected in a two-way fixed effects specification, as year dummies absorb global events such as economic crises, technological change, and international climate agreements.

This model provides a more conservative and causally credible benchmark, indicating that the GDP–emissions relationship weakens once structural and temporal confounders are controlled for.


### Model D: Environmental Kuznets Curve with Fixed Effects


To formally test the Environmental Kuznets Curve (EKC) hypothesis, a quadratic specification in log GDP was estimated including both country and year fixed effects.

Once unobserved heterogeneity across countries and common global shocks over time are controlled for, neither the linear nor the quadratic GDP terms are statistically significant. Moreover, the estimated coefficients do not exhibit the expected inverted-U pattern.

This suggests that the apparent EKC relationship observed in pooled regressions is largely driven by cross-country differences and common time trends rather than a causal income–emissions relationship within countries over time.


### Table 2. Regression Results

Four econometric specifications were estimated to analyze the relationship between economic activity and CO₂ emissions in Mexico and the United States over the period 1990–2023.

- **Model A** estimates total CO₂ emissions using pooled OLS.
- **Model B** models CO₂ emissions per capita.
- **Model C** includes two-way fixed effects (country and year).
- **Model D** tests the Environmental Kuznets Curve (EKC) hypothesis using a quadratic income specification with fixed effects.

All models are estimated using heteroskedasticity-robust (HC3) standard errors.


### Interpretation


The pooled OLS results (Models A and B) suggest a strong association between economic activity and CO₂ emissions. GDP exhibits a positive and statistically significant relationship with emissions, while time trends indicate a gradual reduction in emissions over time, especially in per capita terms.

However, once unobserved heterogeneity is controlled for using country and year fixed effects (Model C), the explanatory power of GDP substantially weakens. This indicates that much of the correlation observed in pooled models is driven by structural differences between countries and common global trends rather than within-country economic dynamics.

The Environmental Kuznets Curve hypothesis is explicitly tested in Model D by including a quadratic income term. The results do not support the existence of an inverted-U relationship between income and emissions once fixed effects are introduced. Neither the linear nor the quadratic income terms are statistically significant, and their signs do not conform to the EKC pattern.


### Conclusion


Overall, the econometric evidence indicates that while economic growth and CO₂ emissions are strongly correlated in pooled specifications, this relationship weakens substantially when accounting for unobserved country-specific and time-specific factors.

The absence of a statistically significant Environmental Kuznets Curve under fixed effects suggests that reductions in emissions are not an automatic outcome of economic growth. Instead, they are more likely driven by structural factors such as technological change, energy composition, and environmental policy.

These findings underscore the importance of institutional and policy interventions in shaping environmental outcomes, rather than relying solely on income-driven mechanisms.

