import os
import sys
import django
import numpy as np

from sentence_transformers import SentenceTransformer

# 🔹 Django setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from movies.models import Movie, MovieEmbedding
from ml.features import prepare_features


def retrain_embeddings():
    print("🔁 Retraining embeddings...")

    df = prepare_features()
    df = df.reset_index(drop=True)

    texts = df["clean_synopsis"].fillna("").tolist()

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts)

    # 🔹 Clear old embeddings
    MovieEmbedding.objects.all().delete()

    for idx, row in df.iterrows():
        movie = Movie.objects.get(id=int(row["id"]))
        MovieEmbedding.objects.create(
            movie=movie,
            vector=embeddings[idx].tolist()
        )

    print("✅ Retraining complete. Embeddings refreshed.")


if __name__ == "__main__":
    retrain_embeddings()
