from fastapi import FastAPI
from app.routers import spotify

app = FastAPI(
    title="OpenSound Analytics API",
    description="API pour analyser des données musicales",
    version="1.0.0"
)

# Liste des routers de traitement ajoutés
app.include_router(spotify.router)

@app.get("/")
def read_root():
    """Page d'accueil de l'API OpenSound"""
    return {
        "message": "Bienvenue sur OpenSound Analytics",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    """Endpoint de vérification de l'état de l'application"""
    return {"status": "healthy"}
