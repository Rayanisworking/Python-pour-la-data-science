from pathlib import Path
import pandas as pd
from download import RAW_ROOT
import json

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_ROOT = PROJECT_ROOT / "data"
CLEANED_ROOT = DATA_ROOT / "cleaned"

OWID_FILE = RAW_ROOT / "owid_mismanaged_plastic_per_capita.csv"
COUNTRY_FILE = RAW_ROOT / "wdi_countries.json"
WDI_FILES = {"infant_mortality_per_1000": RAW_ROOT / "wdi_infant_mortality_2019.json",
    "gdp_pc_ppp_2019": RAW_ROOT / "wdi_gdp_per_capita_ppp_2019.json",
    "basic_sanitation_pct": RAW_ROOT / "wdi_basic_sanitation_2019.json"}

def dataframe_WDI(file_path, name_column):
    with file_path.open("r", encoding="utf-8") as file:
        json_data = json.load(file)

    observations = json_data[1]

    rows = []
    for observation in observations:
        rows.append({
            "iso3": observation["countryiso3code"],
            "year": int(observation["date"]),
            name_column : float(observation["value"]) if observation["value"] is not None else None,
        })

    table = pd.DataFrame(rows)
    return table.loc[table["year"] == 2019] #table_loc garde les lignes où la condition est vraie


def dataframe_country(file_path) :
    with file_path.open("r", encoding="utf-8") as file:
        json_data = json.load(file)

    countries = json_data[1]

    rows = []
    for country in countries:
        region = country.get("region") or {}
        region_id = region.get("id", "")
        region_name = region.get("value", "")
        is_aggregate = (
            str(region_id).upper() in ("", "NA")
            or str(region_name).lower() == "aggregates"
        )
        rows.append({"iso3": (country.get("id")), "country_name": (country.get("name")),
        "region_id": region_id,
        "region_name": region_name,
        "is_aggregate": is_aggregate})

    return pd.DataFrame(rows)

#Séparer pays et régions 

def dataframe_OWID(country_codes) : #renvoie un tuple des dataframes des pays et des régions 
    raw = pd.read_csv(OWID_FILE)

    table = raw[["entity", "code", "year", "mismanaged_plastic_waste_per_capita__kg_per_year"]].copy()
    table.columns = ["entity", "iso3", "year", "plastic_kg_per_person"]
    table["iso3"] = table["iso3"].fillna("").astype(str) #NA devient ""
    table["year"] = pd.to_numeric(table["year"], errors="coerce").astype("Int64") #entiers type pandas (contient les valeurs manquantes)
    table["plastic_kg_per_person"] = pd.to_numeric(table["plastic_kg_per_person"], errors="coerce")

    year_table = table.loc[table["year"] == 2019].copy()
    is_country = year_table["iso3"].isin(country_codes)
    country = year_table.loc[is_country].copy()
    region = year_table.loc[~is_country].copy()

    return country, region

def prepare_project_data():
    missing_files = [
        file_path
        for file_path in [OWID_FILE, COUNTRY_FILE, *WDI_FILES.values()]
        if not file_path.exists()
    ]
    if missing_files:
        names = ", ".join(file_path.name for file_path in missing_files)
        raise FileNotFoundError(
            f"Données brutes manquantes : {names}. "
            "Lancer d'abord `python download.py` depuis la racine du dépôt."
        )

    CLEANED_ROOT.mkdir(parents=True, exist_ok=True)

    country_metadata = dataframe_country(COUNTRY_FILE)
    valid_country_codes = set(country_metadata.loc[(~country_metadata["is_aggregate"]), "iso3"]) 
    valid_country_codes.discard("")

    df_country, df_region = dataframe_OWID(valid_country_codes)

    wdi_tables = {}
    for name_column, file_path in WDI_FILES.items():
        table = dataframe_WDI(file_path, name_column)
        table = table.loc[table["iso3"].isin(valid_country_codes)].copy()
        wdi_tables[name_column] = table

    merged = df_country.copy()

    for name_column, table in wdi_tables.items():
        merged = merged.merge(
            table,
            on=["iso3", "year"],
            how="left",
            validate="one_to_one",
        )

    df_pair = merged.dropna(
        subset=["plastic_kg_per_person", "infant_mortality_per_1000"]).copy()
    
    df_complete = merged.dropna().copy() 
   
    exports = {"merged_2019.csv": merged, "pair_plastic_infant_2019.csv": df_pair, "complete_2019.csv": df_complete, 
            "excluded_2019.csv": df_region,
            "country_metadata.csv": country_metadata}
    for filename, df in exports.items():
        df.to_csv(CLEANED_ROOT / filename, index=False)

    return {"merged": merged,
        "pair_plastic_infant": df_pair,
        "complete": df_complete,
        "excluded": df_region,
        "country_metadata": country_metadata}

if __name__ == "__main__":
    prepare_project_data()
