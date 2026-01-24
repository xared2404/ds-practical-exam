from ds_exam.data.build_dataset import build_panel_mex_usa_1990_2023, save_panel


def main():
    panel = build_panel_mex_usa_1990_2023(1990, 2023)
    print(panel.head())
    print("\nMexico last 3:")
    print(panel[panel["iso3"] == "MEX"].tail(3))
    save_panel(panel)
    print("\nSaved to data/processed/panel_country_year.(parquet|csv)")


if __name__ == "__main__":
    main()
