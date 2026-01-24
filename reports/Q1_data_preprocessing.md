# Data Preprocessing Report

## 1. Objective

The objective of the data preprocessing stage is to construct a clean, consistent, and reproducible country–year panel dataset for Mexico (MEX) and the United States (USA) covering the period 1990–2023. This dataset is used in Question 1 to explore descriptive patterns and relationships between economic activity, population, and carbon dioxide (CO₂) emissions.

The preprocessing pipeline integrates data from multiple sources, harmonizes variable definitions, resolves missing values, and produces derived indicators suitable for analysis.

---

## 2. Data Sources

Three primary data sources are used:

1. **CO₂ Emissions**
   - Source: OWID / World Bank Data360 (Climate and Carbon Budget indicators)
   - Indicator: `OWID_CB_CO2`
   - Unit: Million metric tons of CO₂ (Mt)

2. **Gross Domestic Product (GDP)**
   - Source: World Bank World Development Indicators (WDI)
   - Indicator: `NY.GDP.MKTP.CD`
   - Unit: Current US dollars

3. **Population**
   - Source: World Bank World Development Indicators (WDI)
   - Indicator: `SP.POP.TOTL`
   - Unit: Total population

To ensure reproducibility and avoid network instability, WDI indicators are loaded from locally stored CSV files rather than queried live from the API.

---

## 3. Data Ingestion

### 3.1 CO₂ Data

CO₂ emissions data are loaded from the OWID / Data360 dataset and filtered by:
- Indicator code (`OWID_CB_CO2`)
- ISO3 country codes (`MEX`, `USA`)
- Year range (1990–2023)

The resulting dataset is standardized to the following schema:

| Variable | Description |
|--------|-------------|
| country | Country name |
| iso3 | ISO3 country code |
| year | Calendar year |
| co2_mt | Total CO₂ emissions (million tons) |

---

### 3.2 GDP and Population Data

GDP and population data are extracted from WDI CSV files using a custom loader function. The raw WDI format is reshaped from wide (year columns) to long format and filtered to match the same country set and time window.

The standardized output schema is:

| Variable | Description |
|--------|-------------|
| country | Country name |
| iso3 | ISO3 country code |
| year | Calendar year |
| gdp_current_usd | GDP in current USD |
| population | Total population |

---

## 4. Data Harmonization and Merging

All datasets are harmonized on the common keys:

- `iso3`
- `year`

A left-join strategy is applied starting from the CO₂ dataset to ensure full coverage of emissions observations. GDP and population are merged sequentially.

After merging, the dataset is validated to confirm:
- One observation per country–year
- Balanced panel structure
- No duplicated keys

---

## 5. Feature Engineering

A key derived variable is constructed:

### CO₂ per Capita

\[
\text{CO₂ per capita} = \frac{\text{CO₂ emissions (Mt)} \times 10^6}{\text{Population}}
\]

This transformation converts total emissions into per-person terms, enabling meaningful cross-country comparisons across different population scales.

---

## 6. Missing Data Handling

The preprocessing pipeline explicitly checks for missing values after merging.

- GDP values for the most recent year (2023) were missing in the original WDI dataset and were forward-filled using the latest available observation to preserve panel continuity.
- All remaining variables contain complete data across the full period.

Final validation confirms **zero missing values** in the processed dataset.

---

## 7. Final Dataset Description

The final output is a balanced panel with:

- **Countries:** Mexico, United States
- **Years:** 1990–2023
- **Observations:** 68 (2 countries × 34 years)
- **Variables:**
  - `country`
  - `iso3`
  - `year`
  - `gdp_current_usd`
  - `population`
  - `co2_mt`
  - `co2_per_capita`

The dataset is saved in both CSV and Parquet formats:

## Figures

Key diagnostic figures (saved in `data/processed/`):

- CO₂ per capita timeseries (Mexico, USA):

   ![CO₂ per capita timeseries](../data/processed/co2_per_capita_timeseries.png)

- GDP vs CO₂ per capita scatter:

   ![GDP vs CO₂ per capita](../data/processed/gdp_vs_co2_per_capita.png)

# Data Analysis Report (Q1)

## 1. Dataset Overview

**Panel:** Mexico (MEX) and United States (USA)  
**Period:** 1990–2023  
**Shape:** 68 rows × 7 columns (balanced panel: 2 countries × 34 years)  
**Keys:** `iso3`, `year`  
**Variables:**
- `gdp_current_usd` — GDP (current US$)
- `population` — total population
- `co2_mt` — CO₂ emissions (Mt)
- `co2_per_capita` — CO₂ per capita (tons/person)
- plus identifiers: `country`, `iso3`, `year`

**Missing values:** 0 missing values in the saved parquet (validated with `df.isna().sum()`).

---

## 2. Key Summary Statistics

Below are high-level takeaways (full descriptive table was produced via `groupby("iso3").describe()`):

### Mexico (MEX)
- **GDP:** strong upward trend over time (mean ≈ 1.48e+12 current US$ across 1990–2023)
- **Population:** increasing steadily across the whole period
- **CO₂ (Mt):** rises overall (1990–2023), with a visible drop around 2020 and recovery afterward
- **CO₂ per capita:** relatively stable in a narrow band (max around ~4.42 tons/person)

### United States (USA)
- **GDP:** large and increasing (mean ≈ 1.44e+13 current US$ across 1990–2023)
- **Population:** increasing steadily
- **CO₂ (Mt):** peaks earlier and generally trends downward in later years
- **CO₂ per capita:** notably higher than Mexico throughout the period, with a declining trend in later years (max around ~21.35 tons/person)

**Cross-country contrast:** USA has much higher per-capita emissions; Mexico’s per-capita emissions are lower and comparatively flatter.

---

## 3. Correlation Analysis

Correlations were computed **within each country** over time:

### Mexico (MEX) correlations
- **GDP vs Population:** **0.991** (very strong positive; both trend upward)
- **GDP vs CO₂ (Mt):** **0.893** (strong positive; economic growth co-moves with total emissions)
- **CO₂ (Mt) vs CO₂ per capita:** **0.349** (moderate positive)
- **GDP vs CO₂ per capita:** **-0.095** (near zero; per-capita emissions do not rise much with GDP)

**Interpretation (MEX):** Total emissions increase with scale (GDP + population growth). Per-capita emissions are comparatively stable, suggesting growth is driven more by scale than by increasing per-person emissions intensity.

### United States (USA) correlations
- **GDP vs Population:** **0.990** (very strong positive)
- **GDP vs CO₂ (Mt):** **-0.222** (weak negative)
- **GDP vs CO₂ per capita:** **-0.827** (strong negative)
- **Population vs CO₂ per capita:** **-0.882** (strong negative)
- **CO₂ (Mt) vs CO₂ per capita:** **0.722** (strong positive)

**Interpretation (USA):** Over time, GDP rises while per-capita emissions fall (decoupling). Total emissions also do not increase with GDP (slightly negative correlation), consistent with structural changes, efficiency gains, fuel switching, and policy/technology dynamics.

---

## 4. Visual Pattern: GDP vs CO₂ per Capita

A scatter plot was produced and saved:

- **File:** `data/processed/gdp_vs_co2_per_capita.png`
- **Chart:** GDP (x-axis) vs CO₂ per capita (y-axis), colored by country

**Notable patterns:**
- **Clear separation by country**: USA points cluster at much higher CO₂ per capita than Mexico.
- **Mexico cloud**: relatively flat relationship between GDP and per-capita emissions (weakly negative).
- **USA cloud**: downward slope—higher GDP years tend to have lower CO₂ per capita.

This plot helps communicate the cross-country contrast and supports the correlation findings.

---

## 5. Notable Anomalies / Events

### 2020 shock
Both countries show a clear reduction in CO₂ emissions around **2020**, consistent with a major global disruption year. Mexico’s CO₂ per capita also drops in 2020 and then rebounds.

### Structural change in USA
USA shows a long-run decline in CO₂ per capita despite growing GDP, indicating **economic growth is not mechanically tied to higher per-capita emissions** in this period.

---

## 6. Data Quality Checks

The following checks were performed:
- Balanced panel structure: 34 years per country
- Unique key validation: one row per (`iso3`, `year`)
- Missing values: none in final processed file
- Units consistency:
  - `co2_mt` is treated as **Mt** and converted to tons/person using `* 1e6 / population`
  - `gdp_current_usd` is in current US$

**Result:** Dataset is consistent and ready for modeling in Q2.

---

## 7. Main Takeaways

1. **Scale effects dominate in Mexico:** GDP, population, and total CO₂ emissions move together, while CO₂ per capita stays relatively stable.
2. **Decoupling in the USA:** GDP rises while CO₂ per capita falls strongly, and total CO₂ is weakly negatively related to GDP.
3. **Cross-country gap persists:** USA remains substantially more CO₂-intensive per capita than Mexico throughout 1990–2023.
4. **2020 is a notable discontinuity** that should be considered in modeling (dummy variable, robustness checks, or segmented trends).

---

## 8. Suggested Next Steps (for Q2)

For predictive modeling / regression in Q2, recommended approaches:
- Log-transform GDP and population (or use per-capita GDP)
- Consider time trend and structural break controls (e.g., 2020 dummy)
- Consider country fixed effects if pooling
- Target options:
  - Predict `co2_mt` using `gdp_current_usd`, `population`, year trend
  - Predict `co2_per_capita` using `gdp_per_capita` and year trend
