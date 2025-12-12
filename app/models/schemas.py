from pydantic import BaseModel, Field
from typing import Optional, List, Dict

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

class DeezerTrack(BaseModel):
    """Modèle pour une track du chart Deezer"""

    track: str = Field(
        ...,
        description="Titre de la chanson",
        example="melodrama"
    )
    artist: str = Field(
        ...,
        description="Nom de l'artiste",
        example="disiz"
    )
    genre: Optional[str] = Field(
        None,
        description="Genre musical de la track",
        example="Pop"
    )
    is_explicit_lyrics: bool = Field(
        ...,
        description="Indique si la chanson contient des paroles explicites",
        example=False
    )

    class Config:
        json_schema_extra = {
            "example": {
                "track": "Flowers",
                "artist": "Miley Cyrus",
                "genre": "Pop",
                "is_explicit_lyrics": False
            }
        }


class DeezerChartResponse(BaseModel):
    """Modèle de réponse pour le chart Deezer"""

    total_tracks: int = Field(
        ...,
        description="Nombre total de tracks dans le chart",
        example=10
    )
    tracks: List[DeezerTrack] = Field(
        ...,
        description="Liste des tracks du chart avec leurs métadonnées enrichies"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "total_tracks": 3,
                "tracks": [
                    {
                        "track": "Flowers",
                        "artist": "Miley Cyrus",
                        "genre": "Pop",
                        "is_explicit_lyrics": False
                    },
                    {
                        "track": "Anti-Hero",
                        "artist": "Taylor Swift",
                        "genre": "Pop",
                        "is_explicit_lyrics": False
                    },
                    {
                        "track": "Calm Down",
                        "artist": "Rema",
                        "genre": "Afro Pop",
                        "is_explicit_lyrics": False
                    }
                ]
            }
        }
