from typing import Literal

from fastapi import APIRouter, HTTPException, Query
from app.models.schemas import (
    DurationPopularityCorrelationResponse,
    TopDecadesResponse,
    TopGenresResponse,
)
from src.extractors.extractor_spotify import extract_spotify_data
from src.transformers.transformer_spotify import (
    compute_duration_popularity_correlation,
    get_top_decades_by_popularity,
    get_top_genres_by_popularity,
)

router = APIRouter(
    prefix="/spotify",
    tags=["Spotify Analytics"]
)

# Chemins vers les fichiers CSV (high / low popularity)
DATA_PATHS = {
    "high": "data/raw/high_popularity_spotify_data.csv",
    "low": "data/raw/low_popularity_spotify_data.csv",
}


def _get_data_path(dataset: Literal["high", "low"]) -> str:
    """Retourne le chemin CSV en fonction du dataset choisi."""
    try:
        return DATA_PATHS[dataset]
    except KeyError:
        raise HTTPException(
            status_code=400,
            detail="Paramètre 'dataset' doit être 'high' ou 'low'.",
        )

@router.get("/top-genres", response_model=TopGenresResponse)
def get_top_genres(
    top_n: int = 3,
    dataset: Literal["high", "low"] = Query(
        ...,
        description="Choisir 'high' (high_popularity_spotify_data.csv) ou 'low' (low_popularity_spotify_data.csv)",
    ),
):
    """
    Retourne les N genres musicaux les plus populaires d'après Spotify.

    Args:
        top_n: Nombre de genres à retourner (par défaut 3)

    Returns:
        TopGenresResponse avec les genres et statistiques
    """
    try:
        # Extraction des données
        df = extract_spotify_data(_get_data_path(dataset))

        # Transformation et obtention du résultat
        top_genres = get_top_genres_by_popularity(df, top_n=top_n)

        # Construction de la réponse
        return TopGenresResponse(
            top_genres=top_genres,
            total_tracks_analyzed=len(df)
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Fichier de données introuvable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement: {str(e)}")


@router.get(
    "/duration-popularity-correlation",
    response_model=DurationPopularityCorrelationResponse,
)
def get_duration_popularity_correlation(
    dataset: Literal["high", "low"] = Query(
        ...,
        description="Choisir 'high' (high_popularity_spotify_data.csv) ou 'low' (low_popularity_spotify_data.csv)",
    ),
):
    """
    Retourne la corrélation entre la durée (minutes) et la popularité des morceaux.
    """
    try:
        df = extract_spotify_data(_get_data_path(dataset))
        correlation = compute_duration_popularity_correlation(df)

        return DurationPopularityCorrelationResponse(
            correlation=correlation,
            total_tracks_analyzed=len(df),
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Fichier de données introuvable: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Données invalides pour la corrélation: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement: {str(e)}")


@router.get("/top-decades", response_model=TopDecadesResponse)
def get_top_decades(
    top_n: int = 3,
    dataset: Literal["high", "low"] = Query(
        ...,
        description="Choisir 'high' (high_popularity_spotify_data.csv) ou 'low' (low_popularity_spotify_data.csv)",
    ),
):
    """
    Retourne les décennies les plus populaires (popularité moyenne des morceaux).
    """
    try:
        df = extract_spotify_data(_get_data_path(dataset))
        top_decades = get_top_decades_by_popularity(df, top_n=top_n)

        return TopDecadesResponse(
            top_decades=top_decades,
            total_tracks_analyzed=len(df),
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Fichier de données introuvable: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Données invalides pour les décennies: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement: {str(e)}")
