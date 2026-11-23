from pathlib import Path
import pandas as pd
from download import download,  RAW_ROOT
import json

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_ROOT = PROJECT_ROOT / "data"
CLEANED_ROOT = DATA_ROOT / "cleaned"

OWID_FILE = RAW_ROOT / "owid_mismanaged_plastic_per_capita.csv"
COUNTRY_FILE = RAW_ROOT / "wdi_countries.json"
WDI_FILES = {"infant_mortality_per_1000": RAW_ROOT / "wdi_infant_mortality_2019.json",
    "gdp_pc_ppp_2019": RAW_ROOT / "wdi_gdp_per_capita_ppp_2019.json",
    "basic_sanitation_pct": RAW_ROOT / "wdi_basic_sanitation_2019.json"}

def create_dataframe(file_path, name_column):
    with file_path.open("r", encoding="utf-8") as file:
        json_data = json.load(file)

    observations = json_data[1]

    rows = []
    for observation in observations:
        rows.append({
            "iso3": observation["countryiso3code"],
            "year": int(observation["date"]),
            name_column_column: float(observation["value"]) if observation["value"] is not None else None,
        })

    table = pd.DataFrame(rows)
    return table.loc[table["year"] == 2019] #table_loc garde les lignes où la condition est vraie


def dataframe_country(file_path) :
    with file_path.open("r", encoding="utf-8") as file:
        json_data = json.load(file)

    countries = json_data[1]

    rows = [{"iso3": country["id"],
            "country_name": country["name"],
            "region_id": (country.get("region") or {}).get("id", ""),
            "region_name": (country.get("region") or {}).get("value", "")}
            for country in countries]

    return pd.DataFrame(rows)

#Séparer pays et régions 

def dataframe_OWID(country_codes) : #renvoie un tuple des dataframes des pays et des régions 
    """Charge OWID, garde 2019 et sépare les agrégats"""
    raw = pd.read_csv(OWID_FILE)

    table = raw[[entity_column, code_column, year_column, value_column]].copy()
    table.columns = ["entity", "iso3", "year", "plastic_kg_per_person"]
    table["iso3"] = table["iso3"].fillna("").astype(str)#NA devient ""
    table["year"] = pd.to_numeric(table["year"], errors="coerce").astype("Int64") #entiers type pandas (contient les valeurs manquantes)
    table["plastic_kg_per_person"] = pd.to_numeric(
    table["plastic_kg_per_person"], errors="coerce")

    year_table = table.loc[table["year"] == 2019].copy()
    is_country = year_table["iso3"].isin(country_codes)
    country = year_table.loc[is_country].copy()
    region = year_table.loc[~is_country].copy()

    return country, region


def prepare_project_data():
    CLEANED_ROOT.mkdir(parents=True, exist_ok=True)

    country_metadata = dataframe_country(COUNTRY_FILE)
    valid_country_codes = set(
        country_metadata.loc[~country_metadata["is_aggregate"], "iso3"]
    )
    valid_country_codes.discard("")

    df_country, df_region = dataframe_OWID(valid_country_codes)

    wdi_tables = {}
    for name_column, file_path in WDI_FILES.items():
        table = dataframe_WDI(file_path, value_column)
        table = table.loc[table["iso3"].isin(valid_country_codes)].copy()
        wdi_tables[value_column] = table

    merged = df_country.copy()

    for name_column, table in wdi_tables.items():
        merged = merged.merge(
            table,
            on=["iso3", "year"],
            how="left",
            validate="one_to_one",
        )

    df_pair = merged.dropna(
        subset=["plastic_kg_per_person", "infant_mortality_per_1000"]
    ).copy()
    
    df_complete = merged.dropna().copy()

    return {"merged": merged,
        "pair_plastic_infant": df_pair,
        "complete": df_complete,
        "excluded": df_region,
        "country_metadata": country_metadata}