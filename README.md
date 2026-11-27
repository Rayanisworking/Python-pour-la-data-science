# Déchets plastiques mal gérés et mortalité infantile

**Projet de Python pour la data science — analyse descriptive de l’année 2019**  
**Groupe :** Anton LUCIBELLO, Marius PRIBETICH et Rayan GOMA
**Sujet validé par le chargé de TD.**

## Question de recherche

> En 2019, parmi les pays et territoires disposant des données, observe-t-on une association descriptive entre les déchets plastiques mal gérés par habitant et le taux de mortalité infantile ? Cette association paraît-elle similaire lorsqu’on compare séparément les groupes de PIB par habitant et d’accès à l’assainissement de base ?

Ce projet étudie des indicateurs nationaux pour une seule année. Une association entre ces indicateurs ne prouve pas que les déchets plastiques causent une hausse de la mortalité infantile et ne permet pas de déduire le risque d’un enfant individuellement.

## Résultats principaux

Sur les snapshots téléchargés le **21 novembre 2026**, après exclusion des agrégats et jointure des sources :

- **153** pays/territoires sont appariables aux métadonnées géographiques de la Banque mondiale;
- **151** ont des valeurs pour les déchets plastiques et la mortalité infantile;
- **139** ont des valeurs pour les quatre variables;
- la corrélation de rang de Spearman entre déchets mal gérés par habitant et mortalité infantile est **0,59** sur les 151 observations, et **0,61** sur les 139 cas complets;
- le sens de l’association reste positif dans les groupes de PIB et d’assainissement, mais son ampleur varie.

Ces chiffres sont descriptifs et concernent les snapshots utilisés pour l’analyse locale. Les sources peuvent être mises à jour : pour reproduire exactement ces nombres, il faut utiliser les mêmes fichiers bruts que ceux décrits dans `data/raw/manifest.json`. Les fichiers bruts ne sont pas versionnés dans Git; voir la section [Données et reproductibilité](#données-et-reproductibilité).

Le rapport complet, avec médianes, quartiles et interprétation prudente, est dans [`RAPPORT_RESULTATS_ET_CONCLUSION.md`](RAPPORT_RESULTATS_ET_CONCLUSION.md).

### Figures

**Distribution des deux indicateurs principaux**

![Distribution des déchets plastiques mal gérés et de la mortalité infantile en 2019](outputs/figures/01_distributions.png)

**Déchets plastiques mal gérés et mortalité infantile**

![Nuage de points des déchets plastiques mal gérés et de la mortalité infantile](outputs/figures/02_dechets_mortalite.png)

**Mortalité infantile par quartile de déchets plastiques**

![Mortalité infantile par quartile de déchets plastiques mal gérés](outputs/figures/03_mortalite_par_quartile_dechets.png)

**Association descriptive par groupes de PIB et d’assainissement**

![Corrélation de rang par groupes de PIB et d’assainissement](outputs/figures/04_association_par_groupes.png)

## Données et variables

Le projet combine au moins deux sources ouvertes : Our World in Data (OWID) et les indicateurs World Development Indicators (WDI) de la Banque mondiale.

| Variable utilisée | Source et code | Définition / unité |
|---|---|---|
| Déchets plastiques mal gérés par habitant | [OWID — source Meijer et al. (2021)](https://ourworldindata.org/grapher/mismanaged-plastic-waste-per-capita) | kg par personne et par an. Estimation de déchets plastiques non recyclés, non incinérés ou non conservés dans des décharges étanches. Ce n’est pas une mesure directe de l’exposition individuelle. |
| Mortalité infantile | World Bank WDI `SP.DYN.IMRT.IN` | Décès avant l’âge d’un an pour 1 000 naissances vivantes. Estimation compilée notamment par UN IGME et ses partenaires. |
| PIB par habitant | World Bank WDI `NY.GDP.PCAP.PP.KD` | Dollars internationaux constants de 2021 par habitant, en parité de pouvoir d’achat (PPA). |
| Assainissement de base | World Bank WDI `SH.STA.BASS.ZS` | Pourcentage de la population utilisant au moins un service d’assainissement de base. L’indicateur inclut aussi les services gérés en toute sécurité; il ne mesure pas la collecte des déchets solides. |

Les données sont filtrées à 2019 et reliées à l’aide du code géographique ISO3 et de l’année, pas du nom du territoire. Les agrégats régionaux et mondiaux sont retirés grâce aux métadonnées géographiques de la Banque mondiale. Les valeurs manquantes ne sont ni remplacées par zéro ni imputées.

## Organisation du projet

```text
.
├── README.md
├── requirements.txt
├── GUIDE_EXPLICATION_CODE.md
├── RAPPORT_RESULTATS_ET_CONCLUSION.md
├── notebooks/
│   └── 01_analyse_dechets_mortalite.ipynb
├── src/
│   ├── download_data.py
│   └── prepare_data.py
├── data/
│   ├── README.md
│   ├── raw/          # snapshots locaux, ignorés par Git
│   └── processed/    # tables préparées, ignorées par Git
└── outputs/
    ├── figures/      # graphiques PNG
    └── tables/       # tableaux exportés
```

- [`download_data.py`](src/download_data.py) télécharge les sources publiques, conserve les snapshots bruts et écrit leur provenance dans un manifeste.
- [`prepare_data.py`](src/prepare_data.py) nettoie les tables, vérifie les clés, exclut les agrégats, joint les sources et produit les audits.
- Le [notebook d’analyse](notebooks/01_analyse_dechets_mortalite.ipynb) présente les étapes, les calculs et les graphiques.
- Le [guide d’explication du code](GUIDE_EXPLICATION_CODE.md) explique les commandes terminal, les scripts et les opérations Pandas/Matplotlib pour faciliter l’appropriation du projet par les différents membres du groupe.

## Installation et exécution

Python **3.11** est recommandé. Depuis un terminal ouvert à la racine du dépôt, sous Windows PowerShell :

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src\download_data.py
.\.venv\Scripts\python.exe src\prepare_data.py
.\.venv\Scripts\python.exe -m jupyter lab
```

Chaque membre du groupe crée son propre environnement `.venv`; ce dossier n’est pas envoyé sur GitHub. Les commandes ci-dessus créent l’environnement, installent les dépendances, téléchargent et préparent les données, puis ouvrent JupyterLab. Dans JupyterLab, ouvrir `notebooks/01_analyse_dechets_mortalite.ipynb`, redémarrer le noyau et choisir **Run All**.

Dans un terminal macOS/Linux ou SSP Cloud, les commandes équivalentes sont :

```bash
python3.11 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/download_data.py
.venv/bin/python src/prepare_data.py
.venv/bin/python -m jupyter lab
```

Aucun compte GitHub, jeton d’API ou identifiant personnel n’est nécessaire pour télécharger les sources publiques. Pour l’explication détaillée de chaque commande, consulter [`GUIDE_EXPLICATION_CODE.md`](GUIDE_EXPLICATION_CODE.md).

## Données et reproductibilité

Les scripts enregistrent les snapshots dans `data/raw/` et les tables préparées dans `data/processed/`. Ces deux répertoires sont exclus du dépôt par `.gitignore`, conformément aux consignes de ne pas versionner les jeux de données. Lorsqu’aucun snapshot n’est présent, le script de collecte interroge les API publiques; les données publiées par les fournisseurs peuvent évoluer.

Pour reproduire **exactement** les résultats de ce dépôt :

1. récupérer les mêmes snapshots que ceux décrits dans `data/raw/manifest.json`;
2. les placer sous `data/raw/` ou dans un stockage local/monté accessible;
3. lancer le script de préparation puis le notebook du début à la fin.

Les consignes du cours recommandent de partager les données figées hors Git, par exemple dans l’espace SSP Cloud/S3 du groupe. Le code actuel attend un chemin de dossier local ou monté; il ne lit pas directement une URL `s3://`. Le groupe doit donc suivre la procédure officielle du cours pour monter ou copier les fichiers, et vérifier l’accès du correcteur. La variable `PROJECT_DATA_DIR` peut indiquer un dossier accessible contenant `raw/` et `processed/`. Ne jamais publier de clé, mot de passe, jeton ou URL temporaire privée.

Pour retélécharger volontairement les sources et remplacer les snapshots existants :

```powershell
.\.venv\Scripts\python.exe src\download_data.py --force
```

Cette option crée une nouvelle extraction; elle peut changer les résultats. Après son utilisation, relancer la préparation et le notebook, puis mettre à jour les chiffres et leur date dans le rapport.

## Méthode descriptive

1. Décrire les distributions et les valeurs manquantes avec les effectifs, médianes et quartiles.
2. Examiner le nuage de points entre déchets plastiques mal gérés par habitant et mortalité infantile.
3. Résumer l’association monotone avec la corrélation de rang de Spearman.
4. Comparer la mortalité infantile par quartiles de déchets.
5. Répéter les comparaisons séparément dans les groupes de PIB par habitant et d’accès à l’assainissement, en utilisant les cas complets des quatre variables.
6. Comparer les effectifs et les résultats pour les deux échantillons afin de rendre visible l’effet du choix des données disponibles.

Les ex æquo sont gardés ensemble lors de la création des groupes. Les valeurs extrêmes ne sont pas supprimées automatiquement; elles sont examinées et commentées.

## Limites d’interprétation

- Il s’agit d’une coupe transversale pour 2019, pas d’une analyse de l’évolution dans le temps.
- L’unité d’analyse est un pays ou territoire; les résultats ne permettent pas de tirer une conclusion sur les individus (risque d’erreur écologique).
- Les déchets plastiques mal gérés ne mesurent pas l’exposition réelle des enfants.
- L’indicateur d’assainissement n’est pas un indicateur de collecte ou de traitement des déchets plastiques.
- PIB et assainissement sont des contextes descriptifs, pas des variables qui éliminent tous les facteurs confondants.
- Les données manquantes peuvent limiter la comparabilité et les entités incluses ne représentent pas nécessairement tous les pays/territoires.
- Les corrélations observées ne démontrent pas de causalité.

## Références

- Our World in Data, [Mismanaged plastic waste per capita](https://ourworldindata.org/grapher/mismanaged-plastic-waste-per-capita), données de Meijer et al. (2021), retraitées par OWID.
- World Bank, [métadonnées WDI — mortalité infantile `SP.DYN.IMRT.IN`](https://api.worldbank.org/v2/indicator/SP.DYN.IMRT.IN?format=json).
- World Bank, [métadonnées WDI — PIB/habitant `NY.GDP.PCAP.PP.KD`](https://api.worldbank.org/v2/indicator/NY.GDP.PCAP.PP.KD?format=json).
- World Bank, [métadonnées WDI — assainissement `SH.STA.BASS.ZS`](https://api.worldbank.org/v2/indicator/SH.STA.BASS.ZS?format=json).
- Cours « Python pour la data science », [page Évaluation](https://pythonds.linogaliana.fr/content/annexes/evaluation.html).

