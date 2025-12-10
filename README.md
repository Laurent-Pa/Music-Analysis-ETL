# Music-Analysis-ETL
Cours EPSI : Intégration de données. TP: LabelSound a besoin d'un ETL pour charger des données dans un SID. Ce projet correspond au pipeline automatisé qui met à disposition des endpoints avec des statistiques qui seront consommées par une application Front.


## Structure du repository
```
project/
├── notebooks/          # Chaque dev peut travailler son ETL ici
│   ├── etl_nb_songs_per_genre.ipynb
│   ├── etl_popularity.ipynb
├── src/               # Code modulaire (à remplir progressivement)
│   ├── __init__.py
│   ├── etl/
├── app/               # FastAPI
├── requirements.txt
└── README.md

```

## Installation

1. Cloner le dépôt
```bash
   git clone
   cd Music-Analysis-ETL
```

2. Créer et activer l'environnement virtuel
```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Mac/Linux
   # ou
   .venv\Scripts\activate     # Windows
```

3. Installer les dépendances
```bash
   pip install -r requirements.txt
```

4. Lancer Jupyter
```bash
   jupyter notebook
```
