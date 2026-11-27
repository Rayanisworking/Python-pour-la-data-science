import json
from pathlib import Path
import requests

PROJECT_ROOT  = Path(__file__).resolve().parent #chemin du parent de ce fichier
DATA_ROOT = PROJECT_ROOT / "data"
RAW_ROOT = DATA_ROOT / "raw data"
OWID_CSV_URL = ("https://ourworldindata.org/grapher/mismanaged-plastic-waste-per-capita.csv/?v=1&csvType=full&useColumnShortNames=true")
OWID_META_URL = ("https://ourworldindata.org/grapher/mismanaged-plastic-waste-per-capita.metadata.json/?v=1&csvType=full&useColumnShortNames=true")

WDI_URLS = {
    "infant_mortality": "https://api.worldbank.org/v2/country/all/indicator/SP.DYN.IMRT.IN?date=2019&format=json&per_page=20000",
    "gdp_per_capita_ppp": "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.PP.KD?date=2019&format=json&per_page=20000",
    "basic_sanitation": "https://api.worldbank.org/v2/country/all/indicator/SH.STA.BASS.ZS?date=2019&format=json&per_page=20000",
}
COUNTRY_META_URL = "https://api.worldbank.org/v2/country?format=json&per_page=400"

NE_URL = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"

def download() :
    RAW_ROOT.mkdir(parents=True, exist_ok=True)

    files = [("owid_mismanaged_plastic_per_capita.csv", OWID_CSV_URL, "csv"),
        ("owid_mismanaged_plastic_per_capita.metadata.json", OWID_META_URL, "json"),
        ("wdi_countries.json", COUNTRY_META_URL, "json"), ("ne_110m_admin_0_countries.zip", NE_URL, "zip")]

    for name, url in WDI_URLS.items():
        files.append((f"wdi_{name}_2019.json", url, "json"))

    for filename, url, format in files:
        path = RAW_ROOT / filename

        if format == "json":
            path.write_text(json.dumps(r.json()), encoding="utf-8")
        else:  
            path.write_bytes(r.content)
    
    return RAW_ROOT

if __name__ == "__main__": #pour ne pas que download() s'exécute à l'import, mais que à la demande
    download()