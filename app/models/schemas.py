from pydantic import BaseModel, Field
from typing import Dict

class TopGenresResponse(BaseModel):
    """Modèle de réponse pour les genres les plus populaires"""

    top_genres: Dict[str, float] = Field(
        ...,
        description="Dictionnaire des genres avec leur popularité totale",
        example={"pop": 28575.0, "rock": 17531.0, "hip-hop": 16835.0}
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
                    "pop": 9.0,
                    "rock": 8.0,
                    "hip-hop": 7.0
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

    top_decades: Dict[int, float] = Field(
        ...,
        description="Décennies avec la popularité moyenne des morceaux",
        example={"1990": 65.2, "1980": 62.1, "2000": 60.5},
    )
    total_tracks_analyzed: int = Field(
        ...,
        description="Nombre total de morceaux analysés",
        example=3147,
    )
