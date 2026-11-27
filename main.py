"""Prépare les tables du projet et affiche les effectifs de contrôle.

Avant de lancer ce script, exécuter `python download.py` si les données
brutes ne sont pas encore dans data/raw/.
"""

from cleaning import prepare_project_data


def main():
    """Exécute le nettoyage puis affiche les tailles des échantillons."""
    tables = prepare_project_data()
    print(f"Entités appariables : {len(tables['merged'])}")
    print(f"Déchets + mortalité : {len(tables['pair_plastic_infant'])}")
    print(f"Quatre variables complètes : {len(tables['complete'])}")


if __name__ == "__main__":
    main()
