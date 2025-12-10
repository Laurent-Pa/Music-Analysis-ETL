import pandas as pd
from pathlib import Path

def extract_spotify_data(file_path: str) -> pd.DataFrame:
    """
    Charge les données Spotify depuis un fichier CSV.

    Args:
        file_path: Chemin vers le fichier CSV

    Returns:
        DataFrame contenant les données Spotify

    Raises:
        FileNotFoundError: Si le fichier n'existe pas
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")

    df = pd.read_csv(file_path)
    print(f"✅ Données chargées : {df.shape[0]} lignes, {df.shape[1]} colonnes")

    return df
