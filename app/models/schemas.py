from pydantic import BaseModel, Field
from typing import Dict

class TopGenresResponse(BaseModel):
    """Modèle de réponse pour les genres les plus populaires"""

    top_genres: Dict[str, int] = Field(
        ...,
        description="Dictionnaire des genres avec leur popularité moyenne (score entier)",
        example={"pop": 28, "rock": 17, "hip-hop": 16}
    )

    total_tracks_analyzed: int = Field(
        ...,
        description="Nombre total de morceaux analysés",
        example=1685
    )

    class Config:
        json_schema_extra = {
            "example": {
                "top_genres": {
                    "pop": 28,
                    "rock": 17,
                    "hip-hop": 16
                },
                "total_tracks_analyzed": 999
            }
        }


class DurationPopularityCorrelationResponse(BaseModel):
    """Réponse pour la corrélation durée vs popularité."""

    correlation: float = Field(
        ...,
        description="Coefficient de corrélation entre la durée (min) et la popularité",
        example=0.27,
    )
    total_tracks_analyzed: int = Field(
        ...,
        description="Nombre total de morceaux analysés",
        example=3147,
    )


class TopDecadesResponse(BaseModel):
    """Modèle de réponse pour les décennies les plus populaires."""

    top_decades: Dict[int, int] = Field(
        ...,
        description="Décennies avec la popularité moyenne des morceaux (score entier)",
        example={1990: 65, 1980: 62, 2000: 60},
    )
    total_tracks_analyzed: int = Field(
        ...,
        description="Nombre total de morceaux analysés",
        example=3147,
    )
