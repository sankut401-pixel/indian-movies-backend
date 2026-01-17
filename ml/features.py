import os
import sys
import re
import django
import pandas as pd

# 🔹 Add project root to PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 🔹 Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# 🔹 Import data loader from SAME folder
from ml.data_loader import load_movie_data


def clean_text(text):
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def prepare_features():
    df = load_movie_data()

    # Clean synopsis text
    df["clean_synopsis"] = df["synopsis"].apply(clean_text)

    # Drop rows without rating (important for training)
    df = df.dropna(subset=["rating"])

    return df


if __name__ == "__main__":
    df = prepare_features()
    print(df[["title", "clean_synopsis", "rating"]].head())
