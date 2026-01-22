from __future__ import annotations

from pathlib import Path
import pandas as pd

from ds_exam.data.wb_api import WorldBankClient

from pathlib import Path
import pandas as pd

from ds_exam.data.wb_api import WorldBankClient

def build_panel_mex_usa_1990_2023(year_from: int, year_to: int):
    import pandas as pd

    countries = ["MEX", "USA"]

    # 1) CO2 desde OWID (Mt CO2)
    co2 = load_owid_cb_indicator(
        indicator="OWID_CB_CO2",
        countries_iso3=countries,
        year_from=year_from,
        year_to=year_to,
    ).rename(columns={"value": "co2_mt"})

    # 2) GDP desde OWID
    gdp = load_owid_cb_indicator(
        indicator="OWID_CB_GDP",
        countries_iso3=countries,
        year_from=year_from,
        year_to=year_to,
    ).rename(columns={"value": "gdp_current_usd"})

    # 3) Population desde OWID
    pop = load_owid_cb_indicator(
        indicator="OWID_CB_POPULATION",
        countries_iso3=countries,
        year_from=year_from,
        year_to=year_to,
    ).rename(columns={"value": "population"})

    # 4) Merge panel (evitar country_x / country_y)
    gdp = gdp.drop(columns=["country"], errors="ignore")
    pop = pop.drop(columns=["country"], errors="ignore")

    panel = (
        co2.merge(gdp, on=["iso3", "year"], how="left")
           .merge(pop, on=["iso3", "year"], how="left")
    )

    # 5) CO2 per capita
    panel["co2_per_capita"] = (panel["co2_mt"] * 1e6) / panel["population"]

    # 6) Orden y limpieza final
    panel["year"] = pd.to_numeric(panel["year"], errors="coerce").astype("Int64")
    panel = panel.sort_values(["iso3", "year"]).reset_index(drop=True)

    panel = panel[
        ["country", "iso3", "year", "gdp_current_usd", "population", "co2_mt", "co2_per_capita"]
    ]
    # Si falta GDP en algunos años (ej. 2023), rellenar con el último valor disponible por país
    panel["gdp_current_usd"] = (
    panel.sort_values(["iso3", "year"])
         .groupby("iso3")["gdp_current_usd"]
         .ffill()
)
    return panel

def save_panel(panel: pd.DataFrame) -> None:
    out_dir = Path("data/processed")
    out_dir.mkdir(parents=True, exist_ok=True)

    panel.to_parquet(out_dir / "panel_country_year.parquet", index=False)
    panel.to_csv(out_dir / "panel_country_year.csv", index=False)



from pathlib import Path
from typing import Optional
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]  # repo root
RAW_DIR = ROOT / "data" / "raw" / "worldbank"

def load_owid_cb_indicator(
    indicator: str,
    countries_iso3: list[str] | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
):
    """
    Load a single OWID Carbon Budget indicator from OWID_CB.csv
    and return a tidy panel: country, iso3, year, value.
    """

    import pandas as pd

    path = "data/raw/worldbank/OWID_CB.csv"
    df = pd.read_csv(path)

    required = {
        "REF_AREA",
        "REF_AREA_LABEL",
        "INDICATOR",
        "TIME_PERIOD",
        "OBS_VALUE",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas: {missing}")

    # Filtrar indicador
    df = df[df["INDICATOR"] == indicator].copy()

    # Normalizar columnas
    out = (
        df.rename(
            columns={
                "REF_AREA": "iso3",
                "REF_AREA_LABEL": "country",
                "TIME_PERIOD": "year",
                "OBS_VALUE": "value",
            }
        )[["country", "iso3", "year", "value"]]
        .dropna()
    )

    out["iso3"] = out["iso3"].astype(str).str.strip()
    out["country"] = out["country"].astype(str).str.strip()
    out["year"] = out["year"].astype(int)
    out["value"] = out["value"].astype(float)

    if countries_iso3:
        countries_iso3 = [c.upper() for c in countries_iso3]
        out = out[out["iso3"].isin(countries_iso3)]

    if year_from is not None:
        out = out[out["year"] >= year_from]
    if year_to is not None:
        out = out[out["year"] <= year_to]

    return out.sort_values(["iso3", "year"]).reset_index(drop=True)

def _load_wdi_from_csv(indicator_code: str, countries_iso3: list[str], year_from: int, year_to: int):
    """
    Lee desde el archivo grande WDI (API_19_DS2_en_csv_v2_10104.csv) ya descargado.
    Regresa formato largo: country, iso3, year, value
    """
    import re
    import pandas as pd

    path = "data/raw/worldbank/API_19_DS2_en_csv_v2_10104.csv"

    df = pd.read_csv(path, skiprows=4)
    df.columns = df.columns.astype(str).str.strip()

    # Filtra indicador
    df = df[df["Indicator Code"].astype(str).str.strip() == indicator_code].copy()

    # Filtra países
    df["Country Code"] = df["Country Code"].astype(str).str.strip()
    df = df[df["Country Code"].isin([c.strip().upper() for c in countries_iso3])].copy()

    # Detecta columnas de años "1990", "1991", ...
    year_cols = []
    for c in df.columns:
        c2 = str(c).strip()
        if re.fullmatch(r"\d{4}", c2):
            y = int(c2)
            if year_from <= y <= year_to:
                year_cols.append(c2)

    if not year_cols:
        raise ValueError(f"No encontré columnas de años {year_from}-{year_to} en el CSV WDI.")

    long = df.melt(
        id_vars=["Country Name", "Country Code"],
        value_vars=year_cols,
        var_name="year",
        value_name="value",
    )

    long = long.rename(columns={"Country Name": "country", "Country Code": "iso3"})
    long["year"] = long["year"].astype(int)
    long["value"] = pd.to_numeric(long["value"], errors="coerce")

    return long.sort_values(["iso3", "year"]).reset_index(drop=True)
