import os
import sys
import django

# 🔹 Add project root to PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 🔹 Setup Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# 🔹 Now imports are SAFE
from movies.models import Movie
import pandas as pd


def load_movie_data():
    qs = Movie.objects.all().values(
        "id",
        "title",
        "synopsis",
        "release_date",
        "release_type",
        "rating",
        "created_at",
    )

    df = pd.DataFrame(list(qs))
    return df


if __name__ == "__main__":
    df = load_movie_data()
    print(df.head())
    print("\nDataset shape:", df.shape)
