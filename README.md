# Music-Analysis-ETL
Cours EPSI : Intégration de données. TP: LabelSound a besoin d'un ETL pour charger des données dans un SID. Ce projet correspond au pipeline automatisé qui met à disposition des endpoints avec des statistiques qui seront consommées par une application Front.


## Structure du repository
```
project/
├── .venv              # créé localement par chaque dev
├── app/               # FastAPI
│   ├── models/
│         ├── schemas.py
│   ├── routers/
│         ├── spotify.py
│   ├── main.py
├── data
│   ├── processed
│   ├── raw
├── notebooks/          # Chaque dev peut travailler son ETL ici
│   ├── etl_nb_songs_per_genre.ipynb
│   ├── etl_popularity.ipynb
├── src/               # Code modulaire (à remplir progressivement)
│   ├── __init__.py
│   ├── etl/
│         ├── extractors.py
│         ├── transformers.py
├── .gitignore
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

5. Lancer l'application depuis la console
```bash
   uvicorn app.main:app --reload
```

## Utilisation

### Obtenir les n premiers genres musicaux les plus populaires

#### Requête cURL
```bash
curl -X GET "http://127.0.0.1:8000/spotify/top-genres?top_n=3"
```

#### Requête Python
```python
import requests

response = requests.get("http://127.0.0.1:8000/spotify/top-genres", params={"top_n": 3})
data = response.json()

print(f"Top 3 des genres : {data['top_genres']}")
print(f"Total de morceaux analysés : {data['total_tracks_analyzed']}")
```

#### Réponse attendue (200 OK)
```json
{
  "top_genres": {
    "pop": 28575,
    "rock": 17531,
    "hip-hop": 16835
  },
  "total_tracks_analyzed": 1686
}
```

#### Paramètres
- **top_n** (optionnel) : Nombre de genres à retourner (entre 1 et 10)
  - Par défaut : `3`
  - Exemple : `?top_n=5` pour obtenir le top 5

#### Documentation interactive
Accédez à la documentation complète Swagger UI : http://127.0.0.1:8000/docs
