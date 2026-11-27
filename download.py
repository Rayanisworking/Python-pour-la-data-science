"""Télécharge localement les sources OWID et Banque mondiale.

Les fichiers sont placés dans data/raw/. Un snapshot existant est conservé
par défaut; --force permet de demander explicitement une nouvelle extraction.
"""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import requests


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_ROOT = PROJECT_ROOT / "data"
RAW_ROOT = DATA_ROOT / "raw"
MANIFEST_FILE = DATA_ROOT / "manifest.json"

OWID_CSV_URL = (
    "https://ourworldindata.org/grapher/"
    "mismanaged-plastic-waste-per-capita.csv"
    "?v=1&csvType=full&useColumnShortNames=true"
)
OWID_META_URL = (
    "https://ourworldindata.org/grapher/"
    "mismanaged-plastic-waste-per-capita.metadata.json"
    "?v=1&csvType=full&useColumnShortNames=true"
)

WDI_URLS = {
    "infant_mortality": (
        "https://api.worldbank.org/v2/country/all/indicator/"
        "SP.DYN.IMRT.IN?date=2019&format=json&per_page=20000"
    ),
    "gdp_per_capita_ppp": (
        "https://api.worldbank.org/v2/country/all/indicator/"
        "NY.GDP.PCAP.PP.KD?date=2019&format=json&per_page=20000"
    ),
    "basic_sanitation": (
        "https://api.worldbank.org/v2/country/all/indicator/"
        "SH.STA.BASS.ZS?date=2019&format=json&per_page=20000"
    ),
}
COUNTRY_META_URL = "https://api.worldbank.org/v2/country?format=json&per_page=400"

HEADERS = {"User-Agent": "Python data-science student project"}


def sha256_file(file_path):
    """Retourne une empreinte du fichier pour identifier son contenu."""
    return hashlib.sha256(file_path.read_bytes()).hexdigest()


def list_sources():
    """Construit la liste des fichiers, URL et formats à télécharger."""
    files = [
        ("owid_mismanaged_plastic_per_capita.csv", OWID_CSV_URL, "csv"),
        (
            "owid_mismanaged_plastic_per_capita.metadata.json",
            OWID_META_URL,
            "json",
        ),
        ("wdi_countries.json", COUNTRY_META_URL, "json"),
    ]

    for name, url in WDI_URLS.items():
        files.append((f"wdi_{name}_2019.json", url, "json"))

    return files


def download(force=False):
    """Télécharge les fichiers absents et crée un manifeste de provenance."""
    RAW_ROOT.mkdir(parents=True, exist_ok=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)

    for filename, url, file_format in list_sources():
        file_path = RAW_ROOT / filename

        if file_path.exists() and not force:
            print(f"Snapshot conservé : {file_path.relative_to(PROJECT_ROOT)}")
            continue

        response = requests.get(url, headers=HEADERS, timeout=60)
        response.raise_for_status()

        # Vérifier le JSON avant de l'écrire évite de garder une réponse invalide.
        if file_format == "json":
            response.json()

        file_path.write_bytes(response.content)
        print(f"Téléchargé : {file_path.relative_to(PROJECT_ROOT)}")

    manifest = {
        "description": "Sources publiques et empreintes des snapshots locaux.",
        "manifest_generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "year": 2019,
        "note": (
            "La date ci-dessus est la création du manifeste, pas nécessairement "
            "la date d'extraction initiale des snapshots conservés."
        ),
        "files": [],
    }

    for filename, url, _ in list_sources():
        file_path = RAW_ROOT / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Le fichier source est absent : {file_path}")

        manifest["files"].append(
            {
                "file": filename,
                "url": url,
                "sha256": sha256_file(file_path),
                "size_bytes": file_path.stat().st_size,
            }
        )

    MANIFEST_FILE.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Manifeste créé : {MANIFEST_FILE.relative_to(PROJECT_ROOT)}")
    return RAW_ROOT


def main():
    """Lit --force et lance le téléchargement depuis le terminal."""
    parser = argparse.ArgumentParser(
        description="Télécharge les données OWID et Banque mondiale du projet."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Remplace explicitement les snapshots locaux existants.",
    )
    arguments = parser.parse_args()
    download(force=arguments.force)


if __name__ == "__main__":
    main()
