from fastapi import APIRouter, HTTPException
from app.models.schemas import TopGenresResponse
from src.extractors.extractor_spotify import extract_spotify_data
from src.transformers.transformer_spotify import get_top_genres_by_popularity

router = APIRouter(
    prefix="/spotify",
    tags=["Spotify Analytics"]
)

# Chemin vers ton fichier CSV (à adapter si besoin)
DATA_PATH = "data/raw/high_popularity_spotify_data.csv"

@router.get("/top-genres", response_model=TopGenresResponse)
def get_top_genres(top_n: int = 3):
    """
    Retourne les N genres musicaux les plus populaires d'après Spotify.

    Args:
        top_n: Nombre de genres à retourner (par défaut 3)

    Returns:
        TopGenresResponse avec les genres et statistiques
    """
    try:
        # Extraction des données
        df = extract_spotify_data(DATA_PATH)

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
