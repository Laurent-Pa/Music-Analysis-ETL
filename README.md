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
│   ├── extractors/
│         ├── extractor_spotify.py
│   ├── transformers/
│         ├── transformer_spotify.py
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
curl -X GET "http://127.0.0.1:8000/spotify/top-genres?top_n=3&dataset=high"
```

#### Requête Python
```python
import requests

response = requests.get("http://127.0.0.1:8000/spotify/top-genres", params={"top_n": 3, "dataset": "high"})
data = response.json()

print(f"Top 3 des genres : {data['top_genres']}")
print(f"Total de morceaux analysés : {data['total_tracks_analyzed']}")
```

#### Réponse attendue (200 OK)
```json
{
  "top_genres": {
    "pop": 28,
    "rock": 17,
    "hip-hop": 16
  },
  "total_tracks_analyzed": 1686
}
```

#### Paramètres
- **top_n** (optionnel) : Nombre de genres à retourner (entre 1 et 10)
  - Par défaut : `3`
  - Exemple : `?top_n=5` pour obtenir le top 5
- **dataset** (obligatoire) : Dataset à utiliser
  - Valeurs possibles : `high` ou `low`
  - `high` : utilise `high_popularity_spotify_data.csv`
  - `low` : utilise `low_popularity_spotify_data.csv`
  - Exemple : `?dataset=high` ou `?dataset=low`


### Obtenir le TOP10 des titres du chart Deezer avec genres enrichis

Cet endpoint récupère le chart actuel de Deezer et enrichit chaque track avec son genre musical en interrogeant les informations des albums et genres associés.

#### Requête cURL
```bash
curl -X GET "http://localhost:8000/deezer/chart"
```

#### Requête Python
```python
import requests

response = requests.get("http://127.0.0.1:8000/deezer/chart")
data = response.json()

print(f"Nombre de tracks : {data['total_tracks']}")
print(f"Première track : {data['tracks'][0]}")

# Afficher toutes les tracks avec leurs genres
for track in data['tracks']:
    print(f"🎵 {track['track']} - {track['artist']} | Genre: {track['genre']} | Explicit: {track['is_explicit_lyrics']}")
```

#### Réponse attendue (200 OK)
```json
{
  "total_tracks": 10,
  "tracks": [
    {
      "artist": "Miley Cyrus",
      "artist_picture": "https://api.deezer.com/artist/75798/image",
      "genre": "Pop",
      "is_explicit_lyrics": false,
      "track": "Flowers"
    },
    {
      "artist": "Taylor Swift",
      "artist_picture": "https://api.deezer.com/artist/1191615/image",
      "genre": "Pop",
      "is_explicit_lyrics": false,
      "track": "Anti-Hero"
    },
    {
      "artist": "Rema",
      "artist_picture": "https://api.deezer.com/artist/1191615/image",
      "genre": "Afro Pop",
      "is_explicit_lyrics": false,
      "track": "Calm Down"
    }
  ]
}
```

#### Paramètres
Aucun paramètre requis - cet endpoint retourne automatiquement le chart actuel de Deezer.

#### Notes techniques
- **Source des données** : API publique Deezer (`https://api.deezer.com/chart`)
- **Enrichissement** : Chaque track est enrichie avec son genre musical via des appels supplémentaires aux endpoints `/album/{id}` et `/genre/{id}` de l'API Deezer
- **Optimisation** : Un système de cache LRU est utilisé pour optimiser les appels API répétés (albums et genres identiques)
- **Performance** : Le nombre d'appels API réels dépend du nombre d'albums et de genres uniques dans le chart

#### Codes d'erreur possibles
- **200 OK** : Données récupérées avec succès
- **500 Internal Server Error** : Erreur lors de la récupération ou transformation des données (API Deezer indisponible, erreur de parsing, etc.)
#### Documentation interactive
Accédez à la documentation complète Swagger UI : http://127.0.0.1:8000/docs
