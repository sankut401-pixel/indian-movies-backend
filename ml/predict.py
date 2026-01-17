import os
import sys
import pickle
import torch
import torch.nn as nn
import django
import re

# 🔹 Setup Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


# 🔹 Load vectorizer
with open("ml/models/tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)


# 🔹 Define model architecture (MUST MATCH train.py)
class RatingPredictor(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, 1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x


# 🔹 Load model
model = RatingPredictor(len(vectorizer.get_feature_names_out()))
model.load_state_dict(
    torch.load("ml/models/rating_model.pt", map_location="cpu")
)
model.eval()


def clean_text(text):
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def predict_rating(synopsis: str) -> float:
    cleaned = clean_text(synopsis)
    vec = vectorizer.transform([cleaned]).toarray()
    tensor = torch.tensor(vec, dtype=torch.float32)

    with torch.no_grad():
        pred = model(tensor)

    return round(pred.item(), 2)


if __name__ == "__main__":
    print(predict_rating("A gangster family fights for power in England"))
