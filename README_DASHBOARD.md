# Dashboard Spotify Analytics

Dashboard interactif créé avec Streamlit pour visualiser les statistiques. Ce dashboard utilise les mêmes processus ETL que l'API  (`extractor_spotify`, `transformer_spotify`, etc.).

## Fonctionnalités

Le dashboard affiche plusieurs analyses basées sur les données Spotify :

- **Métriques Globales** : Popularité moyenne/médiane, durée moyenne des morceaux, nombre de genres uniques
- **Top Genres** : Les genres les plus populaires avec graphiques en barres et camemberts
- **Top Décennies** : Les décennies les plus populaires avec visualisations
- **Corrélation Durée vs Popularité** : Analyse de la relation entre la durée des morceaux et leur popularité
- **Distributions** : Histogrammes de la popularité et de la durée des morceaux
- **Statistiques Descriptives** : Tableau récapitulatif avec moyenne, médiane, quartiles, etc.
- **Répartition par Genre** : Nombre de morceaux par genre avec graphiques

## Installation

1. Assurez-vous d'avoir installé les dépendances du projet :
pip install -r requirements.txt

## Utilisation

### Lancer le dashboard

Depuis la racine du projet, exécutez :

'streamlit run dashboard/app.py'

Le dashboard sera accessible dans votre navigateur à l'adresse : `http://localhost:8501`

### Paramètres

Dans la barre latérale, vous pouvez configurer :

- **Dataset CSV** : Choisir entre `high popularity` ou `low popularity`
  - `high` : utilise `data/raw/high_popularity_spotify_data.csv`
  - `low` : utilise `data/raw/low_popularity_spotify_data.csv`

- **Nombre de genres à afficher** : Slider de 1 à 10 (par défaut : 3)

- **Nombre de décennies à afficher** : Slider de 1 à 10 (par défaut : 3)

## Architecture

Le dashboard réutilise les modules ETL existants :

- `src.extractors.extractor_spotify` : Pour charger les données CSV
- `src.transformers.transformer_spotify` : Pour calculer les statistiques
  - `get_top_genres_by_popularity()`
  - `get_top_decades_by_popularity()`
  - `compute_duration_popularity_correlation()`

les résultats affichés dans le dashboard sont identiques à ceux retournés par les endpoints.

## Structure des données

Le dashboard charge les données depuis `data/raw/` et effectue automatiquement :
- Suppression des doublons
- Suppression des valeurs manquantes pour les colonnes essentielles (`track_popularity`, `playlist_genre`)

## Contribution et Workflow Git

### Convention de nommage des branches

Pour les contributions liées au dashboard, suivez la convention de nommage suivante :

**Format** : `dashboard-backup-streamlit/[votre-feature]`

**Exemples** :
- `dashboard-backup-streamlit/add-new-charts` - Pour ajouter de nouveaux graphiques
- `dashboard-backup-streamlit/improve-layout` - Pour améliorer la mise en page
- `dashboard-backup-streamlit/fix-data-loading` - Pour corriger un bug de chargement
- `dashboard-backup-streamlit/add-export-feature` - Pour ajouter une fonctionnalité d'export

**Règles** :
- Utilisez des noms descriptifs en minuscules séparés par des tirets

### Workflow recommandé

1. **Créer une branche depuis `dashboard-backup-streamlit`** :
   
   git checkout -b dashboard-backup-streamlit/votre-feature

2. **Synchroniser avec `main` pour récupérer les dernières modifications** :

   git fetch origin main
   git merge origin/main
      Ou avec rebase (pour un historique plus propre) :
   git rebase origin/main

3. **Développer et tester vos modifications**

4. **Pousser la branche vers le remote** :

   git push -u origin dashboard-backup-streamlit/votre-feature

**Important** : Avant de créer votre PR, assurez-vous d'avoir récupéré les dernières modifications de `main` pour éviter les conflits.

## Notes

- Les données sont mises en cache par Streamlit pour améliorer les performances lors des changements de paramètres
- Le dashboard s'adapte automatiquement au dataset sélectionné
- Tous les graphiques sont interactifs et générés avec matplotlib/seaborn