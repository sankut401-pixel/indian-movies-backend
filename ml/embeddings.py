import os
import sys

# =============================
# 🔹 SAFE ML IMPORTS
# =============================

try:
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity
    from sentence_transformers import SentenceTransformer
    ML_AVAILABLE = True
except Exception:
    ML_AVAILABLE = False

# =============================
# 🔹 Setup Django (SAFE)
# =============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

try:
    import django
    django.setup()
except Exception:
    pass

# =============================
# 🔹 SAFE DJANGO IMPORTS
# =============================

try:
    from movies.models import Movie, MovieEmbedding
    from ml.features import prepare_features
except Exception:
    Movie = None
    MovieEmbedding = None
    prepare_features = None

# =============================
# 🔹 CACHES
# =============================

_embedding_cache = None
_df_cache = None

# =============================
# 🔹 GENERATE EMBEDDINGS
# =============================

def generate_embeddings():
    global _embedding_cache, _df_cache

    # 🚨 Render / ML unavailable
    if not ML_AVAILABLE or prepare_features is None:
        return None, None

    if _embedding_cache is not None and _df_cache is not None:
        return _df_cache, _embedding_cache

    df = prepare_features().reset_index(drop=True)
    texts = df["clean_synopsis"].fillna("").tolist()

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts)

    _df_cache = df
    _embedding_cache = embeddings

    print("✅ Embeddings generated & cached")
    return df, embeddings

# =============================
# 🔹 RECOMMEND BY INDEX (LOCAL USE)
# =============================

def recommend_similar_movies(movie_index, top_n=3):
    df, embeddings = generate_embeddings()
    if df is None:
        return []

    similarity_matrix = cosine_similarity(embeddings)
    scores = similarity_matrix[movie_index]

    similar_indices = scores.argsort()[::-1][1:top_n+1]
    return df.iloc[similar_indices][["title", "rating"]]

# =============================
# 🔹 API-SAFE RECOMMENDATIONS
# =============================

def get_recommendations_for_movie(movie_id, top_n=3):
    df, embeddings = generate_embeddings()
    if df is None:
        return None

    try:
        movie_idx = df.index[df["id"] == movie_id][0]
    except IndexError:
        return None

    similarity_matrix = cosine_similarity(embeddings)
    scores = similarity_matrix[movie_idx]

    results = []
    for idx in scores.argsort()[::-1]:
        if idx == movie_idx:
            continue

        results.append({
            "id": int(df.loc[idx, "id"]),
            "title": df.loc[idx, "title"],
            "rating": float(df.loc[idx, "rating"]) if df.loc[idx, "rating"] else None
        })

        if len(results) == top_n:
            break

    return {
        "movie": df.loc[movie_idx, "title"],
        "recommendations": results
    }

# =============================
# 🔹 SAVE EMBEDDINGS TO DB (LOCAL ONLY)
# =============================

def save_embeddings_to_db():
    if not ML_AVAILABLE or MovieEmbedding is None:
        print("⚠️ ML not available — skipping embedding save")
        return

    df, embeddings = generate_embeddings()

    for idx, row in df.iterrows():
        movie = Movie.objects.get(id=int(row["id"]))
        vector = embeddings[idx].tolist()

        MovieEmbedding.objects.update_or_create(
            movie=movie,
            defaults={"vector": vector}
        )

    print("✅ Embeddings saved to PostgreSQL")

# =============================
# 🔹 LOCAL TEST
# =============================

if __name__ == "__main__":
    save_embeddings_to_db()
