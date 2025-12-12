from pydantic import BaseModel, Field
from typing import Optional, List, Dict

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
    artist_picture: str = Field(
        ...,
        description="Photo de l'artiste",
        example="https://api.deezer.com/artist/292/image"
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
                "artist_picture": " https://api.deezer.com/artist/75798/image",
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
                        "artist_picture": "https://api.deezer.com/artist/75798/image",
                        "genre": "Pop",
                        "is_explicit_lyrics": False
                    },
                    {
                        "track": "Anti-Hero",
                        "artist": "Taylor Swift",
                        "artist_picture": "https://api.deezer.com/artist/1191615/image",
                        "genre": "Pop",
                        "is_explicit_lyrics": False
                    },
                    {
                        "track": "Calm Down",
                        "artist": "Rema",
                        "artist_picture": "https://api.deezer.com/artist/1191615/image",
                        "genre": "Afro Pop",
                        "is_explicit_lyrics": False
                    }
                ]
            }
        }
