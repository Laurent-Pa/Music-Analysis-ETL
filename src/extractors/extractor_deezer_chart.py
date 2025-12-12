import requests
import json
from typing import Dict, Any


def extract_deezer_chart() -> Dict[str, Any]:
    """
    Extrait les données du chart Deezer depuis l'API publique.

    Returns:
        Dict[str, Any]: Données brutes du chart Deezer

    Raises:
        Exception: Si la requête API échoue
    """
    url = "https://api.deezer.com/chart"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print("✅ Données de l'API Deezer Chart récupérées avec succès!")
        print(f"Clés disponibles : {data.keys()}")
        return data
    else:
        raise Exception(f"❌ Erreur lors de la récupération du Chart de l'API Deezer: {response.status_code}")
