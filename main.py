
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors

PROJECT_DIR = Path.cwd()
if not (PROJECT_DIR / "cleaning.py").exists():
    raise FileNotFoundError(
        "Ouvrir Jupyter depuis la racine du dépôt, là où se trouvent cleaning.py et download.py."
    )

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))
PROJECT_DIR = Path.cwd()
if not (PROJECT_DIR / "cleaning.py").exists():
    raise FileNotFoundError(
        "Ouvrir Jupyter depuis la racine du dépôt, là où se trouvent cleaning.py et download.py."
    )

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from cleaning import prepare_project_data
from download import RAW_ROOT

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "#fcfcfd",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#cbd5e1",
    "axes.labelcolor": "#1e293b",
    "axes.titleweight": "bold",
    "xtick.color": "#475569",
    "ytick.color": "#475569",
    "font.size": 10,
})

FIGURES_DIR = PROJECT_DIR / "outputs" / "figures"
from cleaning import prepare_project_data
from download import RAW_ROOT

tables = prepare_project_data()

df_merged = tables["merged"]
import geopandas as gpd
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

variables_cartes = [
    ("plastic_kg_per_person", "Déchets plastiques mal gérés (kg/pers./an)", "Blues"),
    ("infant_mortality_per_1000", "Mortalité infantile (décès / 1 000 naissances)", "YlOrRd"),
    ("gdp_pc_ppp_2019", "PIB / habitant (dollars int. PPA 2021)", "BuGn"),
    ("basic_sanitation_pct", "Assainissement de base (% population)", "Purples"),
]

world = gpd.read_file("https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip")
world["iso3"] = world["ADM0_A3"].where(world["ADM0_A3"] != "-99", world["ISO_A3"])
world = world[world["iso3"] != "ATA"]

gdf = world.merge(df_merged, on="iso3", how="left").to_crs("ESRI:54035")

fig, axes = plt.subplots(2, 2, figsize=(15, 9))
axes = axes.flatten()

gris = "#475569"
patch_gris = mpatches.Patch(facecolor=gris, edgecolor="white", label="Pays sans données")

for ax, (col, titre, cmap) in zip(axes, variables_cartes):
    vals = gdf[col].dropna()
    # Décale l'échelle vers les valeurs basses/moyennes (gamma > 1 = moins de saturation foncée)
    norm = mcolors.PowerNorm(gamma=0.35, vmin=vals.min(), vmax=vals.max())

    gdf.plot(ax=ax, color=gris, edgecolor="white", linewidth=0.3)
    gdf.dropna(subset=[col]).plot(
        column=col, ax=ax, cmap=cmap, norm=norm, edgecolor="white", linewidth=0.3, legend=False
    )

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm, ax=ax, shrink=0.65, pad=0.02)
    ax.legend(handles=[patch_gris], loc="lower left", fontsize=8)
    ax.set_title(titre, fontsize=10.5)
    ax.set_axis_off()

plt.tight_layout()
plt.savefig(FIGURES_DIR / "fig2_cartes_mondiales_2019.png", dpi=150, bbox_inches="tight")
plt.show()