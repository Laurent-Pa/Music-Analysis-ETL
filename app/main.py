from fastapi import FastAPI
from app.routers import spotify

app = FastAPI(
    title="Spotify Analytics API",
    description="API pour analyser les données Spotify",
    version="1.0.0"
)

# Liste des routers de traitement ajoutés
app.include_router(spotify.router)

@app.get("/")
def read_root():
    """Page d'accueil de l'API"""
    return {
        "message": "Bienvenue sur l'API Spotify Analytics",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    """Endpoint de vérification de santé"""
    return {"status": "healthy"}
