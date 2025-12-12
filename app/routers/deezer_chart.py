from fastapi import APIRouter, HTTPException
from app.models.schemas import DeezerChartResponse
from src.extractors.extractor_deezer_chart import extract_deezer_chart
from src.transformers.transformer_deezer_chart import transform_deezer_chart

router = APIRouter(
    prefix="/deezer",
    tags=["Deezer"]
)


@router.get("/chart", response_model=DeezerChartResponse)
def get_deezer_chart():
    """
    Récupère le chart Deezer avec les genres enrichis.

    Ce endpoint interroge l'API Deezer pour obtenir le chart actuel,
    puis enrichit chaque track avec son genre musical en récupérant
    les informations des albums et genres associés.

    Returns:
        DeezerChartResponse: Liste des tracks du chart avec métadonnées enrichies

    Raises:
        HTTPException: En cas d'erreur lors de la récupération ou transformation des données
    """
    try:
        # Extraction des données brutes
        raw_data = extract_deezer_chart()

        # Transformation et enrichissement en associant le genre au titre
        transformed_data = transform_deezer_chart(raw_data)

        return {
            "total_tracks": len(transformed_data),
            "tracks": transformed_data
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération du chart Deezer: {str(e)}"
        )
