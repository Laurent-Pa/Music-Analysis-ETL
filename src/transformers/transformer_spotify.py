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


def compute_duration_popularity_correlation(df: pd.DataFrame) -> float:
    """
    Calcule la corrélation entre la durée (en minutes) et la popularité des morceaux.

    Args:
        df: DataFrame Spotify contenant les colonnes 'duration_ms' et 'track_popularity'

    Returns:
        Corrélation (float) entre la durée et la popularité.

    Raises:
        ValueError: Si les colonnes requises sont absentes, ou si la corrélation est indéfinissable.
    """
    required_columns = {"duration_ms", "track_popularity"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Colonnes manquantes pour le calcul de corrélation: {missing}")

    df_clean = df[list(required_columns)].dropna()
    if df_clean.empty:
        raise ValueError("Impossible de calculer la corrélation: aucune donnée valide après nettoyage.")

    # Conversion en minutes pour plus de lisibilité
    df_clean = df_clean.assign(duration_min=df_clean["duration_ms"] / 60000)
    corr = df_clean[["duration_min", "track_popularity"]].corr().iloc[0, 1]

    if pd.isna(corr):
        raise ValueError("Corrélation indéfinie (données constantes ou insuffisantes).")

    return float(corr)


def get_top_decades_by_popularity(df: pd.DataFrame, top_n: int = 3) -> Dict[int, float]:
    """
    Retourne les décennies les plus populaires selon la popularité moyenne des morceaux.

    Args:
        df: DataFrame Spotify contenant 'track_album_release_date' et 'track_popularity'
        top_n: Nombre de décennies à retourner

    Returns:
        Dictionnaire {decade: popularité_moyenne}
    """
    required_columns = {"track_album_release_date", "track_popularity"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Colonnes manquantes pour le calcul de popularité par décennie: {missing}")

    df_clean = df[list(required_columns)].dropna()
    if df_clean.empty:
        raise ValueError("Aucune donnée valide pour calculer la popularité par décennie.")

    # Conversion en année puis en décennie
    df_clean = df_clean.assign(
        release_year=pd.to_datetime(df_clean["track_album_release_date"], errors="coerce").dt.year
    )
    df_clean = df_clean.dropna(subset=["release_year"])
    if df_clean.empty:
        raise ValueError("Impossible de déterminer les années de sortie après conversion.")

    df_clean = df_clean.assign(decade=(df_clean["release_year"] // 10) * 10)

    decade_popularity = (
        df_clean.groupby("decade")["track_popularity"].mean().sort_values(ascending=False)
    )

    top_decades = decade_popularity.head(top_n)

    return {int(decade): float(popularity) for decade, popularity in top_decades.items()}
