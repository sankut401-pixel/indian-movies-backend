import os
import sys
import django
import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

_embedding_cache = None
_df_cache = None

# 🔹 STEP 1: Add project root to PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 🔹 STEP 2: Setup Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# 🔹 STEP 3: Now SAFE to import Django models
from movies.models import Movie, MovieEmbedding
from ml.features import prepare_features

def generate_embeddings():
    global _embedding_cache, _df_cache

    if _embedding_cache is not None and _df_cache is not None:
        return _df_cache, _embedding_cache

    df = prepare_features()
    df = df.reset_index(drop=True)

    texts = df["clean_synopsis"].fillna("").tolist()

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts)

    _df_cache = df
    _embedding_cache = embeddings

    print("✅ Embeddings generated & cached")

    return df, embeddings


def recommend_similar_movies(movie_index, top_n=3):
    df, embeddings = generate_embeddings()

    similarity_matrix = cosine_similarity(embeddings)

    scores = similarity_matrix[movie_index]
    similar_indices = np.argsort(scores)[::-1][1:top_n+1]

    return df.iloc[similar_indices][["title", "rating"]]

if __name__ == "__main__":
    recommendations = recommend_similar_movies(movie_index=0)
    print("\nRecommended Movies:")
    print(recommendations)

def get_recommendations_for_movie(movie_id, top_n=3):
    df, embeddings = generate_embeddings()

    # 🔹 Reset index so embeddings & df align
    df = df.reset_index(drop=True)

    # 🔹 Find movie inside embedding dataset
    try:
        movie_idx = df.index[df["id"] == movie_id][0]
    except IndexError:
        # Movie exists in DB but not in ML dataset
        return None

    similarity_matrix = cosine_similarity(embeddings)
    scores = similarity_matrix[movie_idx]

    similar_indices = (
        scores.argsort()[::-1]
        .tolist()
    )

    results = []
    for idx in similar_indices:
        if idx == movie_idx:
            continue
        results.append({
            "id": int(df.loc[idx, "id"]),
            "title": df.loc[idx, "title"],
            "rating": float(df.loc[idx, "rating"])
        })
        if len(results) == top_n:
            break

    return {
        "movie": df.loc[movie_idx, "title"],
        "recommendations": results
    }

def save_embeddings_to_db():
    df, embeddings = generate_embeddings()

    for idx, row in df.iterrows():
        movie_id = int(row["id"])
        vector = embeddings[idx].tolist()

        movie = Movie.objects.get(id=movie_id)

        MovieEmbedding.objects.update_or_create(
            movie=movie,
            defaults={"vector": vector}
        )

    print("✅ Embeddings saved to PostgreSQL")

if __name__ == "__main__":
    save_embeddings_to_db()

