# Extractions World Bank (2019)

Projet : association entre déchets plastiques mal gérés par habitant et mortalité infantile.

Chaque série est extraite pour 2019 depuis l’API World Bank. Le JSON brut est conservé et le CSV est une version aplatie pour analyse. Les agrégats régionaux et valeurs manquantes sont conservés à ce stade, pour que le nettoyage du projet soit traçable.

| Fichier | Indicateur | Code WDI | Unité |
|---|---|---|---|
| wdi_2019_mortalite_infantile.csv | Mortalité infantile, avant 1 an | SP.DYN.IMRT.IN | décès pour 1 000 naissances vivantes |
| wdi_2019_pib_habitant_ppa.csv | PIB par habitant, PPA constante 2021 | NY.GDP.PCAP.PP.KD | dollars internationaux constants par habitant |
| wdi_2019_assainissement_base.csv | Population utilisant au moins un service d’assainissement de base | SH.STA.BASS.ZS | pourcentage de la population |

Les fichiers JSON correspondants sont dans data/raw. Les CSV comportent les colonnes country, country_iso3, year, value, unit, indicator_code, indicator_name, observation_status et decimal.

## Nettoyage prévu

1. Écarter les agrégats régionaux et conserver les pays avec un code ISO3 valide.
2. Vérifier doublons, valeurs manquantes et types.
3. Fusionner sur country_iso3 et year, puis mesurer le chevauchement avec le CSV OWID de déchets plastiques.
4. Documenter les exclusions et ne pas imputer automatiquement les valeurs manquantes.

Endpoints utilisés :
- https://api.worldbank.org/v2/country/all/indicator/SP.DYN.IMRT.IN?date=2019&format=json&per_page=20000
- https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.PP.KD?date=2019&format=json&per_page=20000
- https://api.worldbank.org/v2/country/all/indicator/SH.STA.BASS.ZS?date=2019&format=json&per_page=20000

Extrait le 23 octobre 2026.