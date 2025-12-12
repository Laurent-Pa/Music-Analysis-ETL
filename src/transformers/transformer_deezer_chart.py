import pandas as pd
import requests
from typing import Dict, Any, List, Optional
from functools import lru_cache


@lru_cache(maxsize=500)
def get_album_genre(album_id: int) -> Optional[int]:
    """
    Récupère le genre_id d'un album avec mise en cache.

    Args:
        album_id: ID de l'album Deezer

    Returns:
        int: ID du genre ou None si non trouvé
    """
    try:
        url = f"https://api.deezer.com/album/{album_id}"
        response = requests.get(url)
        if response.status_code == 200:
            album_data = response.json()
            genres = album_data.get('genres', {}).get('data', [])
            if genres:
                return genres[0].get('id', None)
        return None
    except Exception as e:
        print(f"⚠️ Erreur album {album_id}: {e}")
        return None


@lru_cache(maxsize=100)
def get_genre_name(genre_id: Optional[int]) -> Optional[str]:
    """
    Récupère le nom d'un genre à partir de son ID avec mise en cache.

    Args:
        genre_id: ID du genre Deezer

    Returns:
        str: Nom du genre ou None si non trouvé
    """
    if genre_id is None:
        return None
    try:
        url = f"https://api.deezer.com/genre/{genre_id}"
        response = requests.get(url)
        if response.status_code == 200:
            genre_data = response.json()
            return genre_data.get('name', None)
        return None
    except Exception as e:
        print(f"⚠️ Erreur genre {genre_id}: {e}")
        return None


def transform_deezer_chart(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Transforme les données brutes du chart Deezer en format exploitable.
    Utilise un cache pour optimiser les appels API répétés.

    Args:
        data: Données brutes de l'API Deezer Chart

    Returns:
        List[Dict]: Liste des tracks avec leurs métadonnées enrichies
    """
    # Extraire les tracks
    tracks_data = data['tracks']['data']

    # Normaliser les données (aplatir les objets imbriqués)
    df_tracks_normalized = pd.json_normalize(tracks_data)
    print(f"📊 {len(df_tracks_normalized)} tracks à traiter")

    # Sélectionner les colonnes pertinentes
    df_tracks_filtered = df_tracks_normalized[[
        'title',
        'artist.name',
        'artist.picture',
        'album.id',
        'explicit_lyrics'
    ]].copy()

    # Récupérer les albums uniques pour optimiser les appels
    unique_albums = df_tracks_filtered['album.id'].unique()
    print(f"🔍 Récupération des genres pour {len(unique_albums)} albums uniques...")

    # Appliquer la fonction avec cache
    df_tracks_filtered['genre_id'] = df_tracks_filtered['album.id'].apply(
        lambda album_id: get_album_genre(album_id)
    )

    # Récupérer les genres uniques
    unique_genres = df_tracks_filtered['genre_id'].dropna().unique()
    print(f"🎵 Récupération des noms pour {len(unique_genres)} genres uniques...")

    df_tracks_filtered['genre_name'] = df_tracks_filtered['genre_id'].apply(
        lambda genre_id: get_genre_name(genre_id)
    )

    # Créer le DataFrame final avec les colonnes renommées
    df_tracks_final = df_tracks_filtered[[
        'title',
        'artist.name',
        'artist.picture',
        'genre_name',
        'explicit_lyrics'
    ]].copy()

    df_tracks_final.columns = ['track', 'artist', 'artist_picture','genre', 'is_explicit_lyrics']

    # Convertir en liste de dictionnaires
    result = df_tracks_final.to_dict(orient='records')

    return result


def clear_cache():
    """Vide le cache des fonctions de récupération de genres."""
    get_album_genre.cache_clear()
    get_genre_name.cache_clear()
    print("🗑️ Cache vidé")
