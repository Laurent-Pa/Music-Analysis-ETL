import pandas as pd
from typing import Dict

def get_top_genres_by_popularity(df: pd.DataFrame, top_n: int = 3) -> Dict[str, float]:
    """
    Nettoie les données et retourne les N genres les plus populaires.

    Args:
        df: DataFrame Spotify contenant les colonnes 'playlist_genre' et 'track_popularity'
        top_n: Nombre de genres à retourner (par défaut 3)

    Returns:
        Dictionnaire {genre: popularité_totale} des top N genres
    """
    # Copie pour ne pas modifier l'original
    df_clean = df.copy()

    # Supprimer les doublons
    nb_doublons = df_clean.duplicated().sum()
    df_clean = df_clean.drop_duplicates()
    print(f"🔄 {nb_doublons} doublons supprimés")

    # Supprimer les valeurs manquantes
    nb_lignes_avant = len(df_clean)
    df_clean = df_clean.dropna()
    nb_lignes_supprimees = nb_lignes_avant - len(df_clean)
    print(f"🗑️ {nb_lignes_supprimees} lignes avec valeurs manquantes supprimées")

    print(f"✅ Dataset final : {df_clean.shape[0]} lignes, {df_clean.shape[1]} colonnes")

    # Calculer la popularité totale par genre
    popularity_by_genre = df_clean.groupby('playlist_genre')['track_popularity'].sum()

    # Trier et prendre les top N
    top_genres = popularity_by_genre.sort_values(ascending=False).head(top_n)

    return top_genres.to_dict()
