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
    "gdp_pc_ppp_2021": RAW_ROOT / "wdi_gdp_per_capita_ppp_2019.json",
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
            value_column: float(observation["value"]) if observation["value"] is not None else None,
        })

    table = pd.DataFrame(rows)
    return table.loc[table["year"] == 2019] #table_loc garde les lignes où la condition est vraie


def dataframe_country(file_path) :
    with file_path.open("r", encoding="utf-8") as file:
        json_data = json.load(file)

    countries = json_data[1]

    rows = [{"iso3": country["id"].upper(),
            "country_name": country["name"],
            "region_id": (country.get("region") or {}).get("id", ""),
            "region_name": (country.get("region") or {}).get("value", "")}
            for country in countries]

    return pd.DataFrame(rows)       