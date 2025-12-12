import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# Ajoute la racine du projet au PYTHONPATH pour réutiliser les modules existants.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.extractors.extractor_spotify import extract_spotify_data
from src.transformers.transformer_spotify import (
    compute_duration_popularity_correlation,
    get_top_decades_by_popularity,
    get_top_genres_by_popularity,
)

# Configuration du style matplotlib
try:
    plt.style.use("seaborn-v0_8-darkgrid")
except OSError:
    plt.style.use("seaborn-darkgrid")
sns.set_palette("husl")

DATASETS = {
    "high": ROOT_DIR / "data" / "raw" / "high_popularity_spotify_data.csv",
    "low": ROOT_DIR / "data" / "raw" / "low_popularity_spotify_data.csv",
}


@st.cache_data(show_spinner=False)
def load_dataset(key: str) -> pd.DataFrame:
    path = DATASETS[key]
    return extract_spotify_data(str(path))


def main() -> None:
    st.set_page_config(
        page_title="Spotify Analytics Dashboard",
        layout="wide",
    )
    st.title("Dashboard Spotify Analytics")
    st.caption("Basé sur les mêmes traitements que les endpoints FastAPI.")

    st.sidebar.header("Paramètres")
    dataset_key = st.sidebar.selectbox(
        "Dataset CSV",
        options=list(DATASETS.keys()),
        format_func=lambda k: f"{k} popularity",
        index=0,
    )
    top_n_genres = st.sidebar.slider("Nombre de genres à afficher", 1, 10, 3)
    top_n_decades = st.sidebar.slider("Nombre de décennies à afficher", 1, 10, 3)

    try:
        df = load_dataset(dataset_key)
    except FileNotFoundError as e:
        st.error(f"Fichier introuvable : {e}")
        st.stop()
    except Exception as e:  # pragma: no cover - affichage Streamlit
        st.error(f"Impossible de charger les données : {e}")
        st.stop()

    # Nettoyage des données
    df_clean = df.copy()
    df_clean = df_clean.drop_duplicates()
    df_clean = df_clean.dropna(subset=["track_popularity", "playlist_genre"])

    st.success(
        f"Dataset chargé : **{DATASETS[dataset_key].name}** "
        f"({df_clean.shape[0]:,} morceaux, {df_clean.shape[1]} colonnes)"
    )

    # ========== MÉTRIQUES GLOBALES ==========
    st.header("Métriques Globales")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_popularity = df_clean["track_popularity"].mean()
        st.metric("Popularité moyenne", f"{avg_popularity:.1f}")
    
    with col2:
        median_popularity = df_clean["track_popularity"].median()
        st.metric("Popularité médiane", f"{median_popularity:.1f}")
    
    with col3:
        if "duration_ms" in df_clean.columns:
            avg_duration_min = (df_clean["duration_ms"].mean() / 60000)
            st.metric("Durée moyenne", f"{avg_duration_min:.1f} min")
        else:
            st.metric("Durée moyenne", "N/A")
    
    with col4:
        unique_genres = df_clean["playlist_genre"].nunique()
        st.metric("Genres uniques", f"{unique_genres}")

    st.divider()

    # ========== TOP GENRES ==========
    st.header("Top Genres")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        try:
            top_genres = get_top_genres_by_popularity(df, top_n=top_n_genres)
            genres_df = (
                pd.DataFrame(top_genres.items(), columns=["Genre", "Popularité moyenne"])
                .sort_values("Popularité moyenne", ascending=False)
                .reset_index(drop=True)
            )
            
            # Graphique en barres
            st.bar_chart(genres_df.set_index("Genre"), height=300)
        except Exception as e:
            st.error(f"Erreur sur les genres : {e}")
    
    with col2:
        try:
            # Graphique en camembert
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(
                genres_df["Popularité moyenne"],
                labels=genres_df["Genre"],
                autopct="%1.1f%%",
                startangle=90,
            )
            ax.set_title("Répartition des genres", fontsize=12, fontweight="bold")
            st.pyplot(fig)
            plt.close()
        except Exception as e:
            st.error(f"Erreur sur le camembert : {e}")

    # Statistiques par genre
    try:
        genre_stats = df_clean.groupby("playlist_genre")["track_popularity"].agg([
            ("Moyenne", "mean"),
            ("Médiane", "median"),
            ("Écart-type", "std"),
            ("Nombre de morceaux", "count")
        ]).round(2).sort_values("Moyenne", ascending=False)
        st.subheader("Statistiques détaillées par genre")
        st.dataframe(genre_stats, use_container_width=True)
    except Exception as e:
        st.error(f"Erreur sur les statistiques par genre : {e}")

    st.divider()

    # ========== TOP DÉCENNIES ==========
    st.header("Top Décennies")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        try:
            top_decades = get_top_decades_by_popularity(df, top_n=top_n_decades)
            decades_df = (
                pd.DataFrame(top_decades.items(), columns=["Décennie", "Popularité moyenne"])
                .sort_values("Popularité moyenne", ascending=False)
                .reset_index(drop=True)
            )
            decades_df["Décennie"] = decades_df["Décennie"].astype(str)
            
            # Graphique en barres
            st.bar_chart(decades_df.set_index("Décennie"), height=300)
        except Exception as e:
            st.error(f"Erreur sur les décennies : {e}")
    
    with col2:
        try:
            # Graphique en camembert
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(
                decades_df["Popularité moyenne"],
                labels=decades_df["Décennie"],
                autopct="%1.1f%%",
                startangle=90,
            )
            ax.set_title("Répartition des décennies", fontsize=12, fontweight="bold")
            st.pyplot(fig)
            plt.close()
        except Exception as e:
            st.error(f"Erreur sur le camembert : {e}")

    st.divider()

    # ========== CORRÉLATION DURÉE VS POPULARITÉ ==========
    st.header("Corrélation Durée vs Popularité")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            correlation = compute_duration_popularity_correlation(df)
            st.metric("Coefficient de corrélation", f"{correlation:.3f}")
            st.caption(
                "Valeur entre -1 et 1 :\n"
                "• Proche de 1 = corrélation positive forte\n"
                "• Proche de 0 = pas de corrélation\n"
                "• Proche de -1 = corrélation négative forte"
            )
        except Exception as e:
            st.error(f"Erreur sur la corrélation : {e}")
    
    with col2:
        try:
            if "duration_ms" in df_clean.columns:
                df_plot = df_clean[["duration_ms", "track_popularity"]].dropna()
                df_plot["duration_min"] = df_plot["duration_ms"] / 60000
                
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.scatter(
                    df_plot["duration_min"],
                    df_plot["track_popularity"],
                    alpha=0.5,
                    s=20
                )
                ax.set_xlabel("Durée (minutes)", fontsize=11)
                ax.set_ylabel("Popularité", fontsize=11)
                ax.set_title("Relation Durée vs Popularité", fontsize=12, fontweight="bold")
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                plt.close()
        except Exception as e:
            st.error(f"Erreur sur le graphique de corrélation : {e}")

    st.divider()

    # ========== DISTRIBUTIONS ==========
    st.header("Distributions")
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            st.subheader("Distribution de la popularité")
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.hist(df_clean["track_popularity"], bins=30, edgecolor="black", alpha=0.7)
            ax.axvline(avg_popularity, color="red", linestyle="--", linewidth=2, label=f"Moyenne: {avg_popularity:.1f}")
            ax.set_xlabel("Popularité", fontsize=11)
            ax.set_ylabel("Fréquence", fontsize=11)
            ax.set_title("Histogramme de la popularité", fontsize=12, fontweight="bold")
            ax.legend()
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            plt.close()
        except Exception as e:
            st.error(f"Erreur sur la distribution de popularité : {e}")
    
    with col2:
        try:
            if "duration_ms" in df_clean.columns:
                st.subheader("Distribution de la durée")
                df_duration = df_clean["duration_ms"].dropna() / 60000  # Conversion en minutes
                fig, ax = plt.subplots(figsize=(8, 5))
                ax.hist(df_duration, bins=30, edgecolor="black", alpha=0.7)
                ax.axvline(df_duration.mean(), color="red", linestyle="--", linewidth=2, 
                          label=f"Moyenne: {df_duration.mean():.1f} min")
                ax.set_xlabel("Durée (minutes)", fontsize=11)
                ax.set_ylabel("Fréquence", fontsize=11)
                ax.set_title("Histogramme de la durée", fontsize=12, fontweight="bold")
                ax.legend()
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                plt.close()
        except Exception as e:
            st.error(f"Erreur sur la distribution de durée : {e}")

    # ========== STATISTIQUES DESCRIPTIVES ==========
    st.divider()
    st.header("Statistiques Descriptives")
    
    try:
        numeric_cols = ["track_popularity"]
        if "duration_ms" in df_clean.columns:
            numeric_cols.append("duration_ms")
        if "energy" in df_clean.columns:
            numeric_cols.append("energy")
        if "danceability" in df_clean.columns:
            numeric_cols.append("danceability")
        if "tempo" in df_clean.columns:
            numeric_cols.append("tempo")
        
        stats_df = df_clean[numeric_cols].describe()
        if "duration_ms" in stats_df.columns:
            # Convertir duration_ms en minutes pour l'affichage
            stats_df["duration_min"] = stats_df["duration_ms"] / 60000
            stats_df = stats_df.drop(columns=["duration_ms"])
        
        st.dataframe(stats_df, use_container_width=True)
    except Exception as e:
        st.error(f"Erreur sur les statistiques descriptives : {e}")

    # ========== RÉPARTITION PAR GENRE (nombre de morceaux) ==========
    st.divider()
    st.header("Répartition du nombre de morceaux par genre")
    
    try:
        genre_counts = df_clean["playlist_genre"].value_counts().sort_values(ascending=False)
        genre_counts_df = pd.DataFrame({
            "Genre": genre_counts.index,
            "Nombre de morceaux": genre_counts.values
        })
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.bar_chart(genre_counts_df.set_index("Genre"), height=300)
        
        with col2:
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(
                genre_counts_df["Nombre de morceaux"],
                labels=genre_counts_df["Genre"],
                autopct="%1.1f%%",
                startangle=90,
            )
            ax.set_title("Répartition par genre", fontsize=12, fontweight="bold")
            st.pyplot(fig)
            plt.close()
    except Exception as e:
        st.error(f"Erreur sur la répartition par genre : {e}")


if __name__ == "__main__":
    main()

