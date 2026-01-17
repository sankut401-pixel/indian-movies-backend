import os
import sys
import re

# =============================
# 🔹 SAFE ML IMPORTS
# =============================

try:
    import torch
    import torch.nn as nn
    import pickle
    TORCH_AVAILABLE = True
except Exception:
    TORCH_AVAILABLE = False

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
# 🔹 LOAD ML ONLY IF AVAILABLE
# =============================

vectorizer = None
model = None

if TORCH_AVAILABLE:
    try:
        # Load vectorizer
        with open("ml/models/tfidf_vectorizer.pkl", "rb") as f:
            vectorizer = pickle.load(f)

        # Define model (same as training)
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

        model = RatingPredictor(len(vectorizer.get_feature_names_out()))
        model.load_state_dict(
            torch.load("ml/models/rating_model.pt", map_location="cpu")
        )
        model.eval()

    except Exception as e:
        print("⚠️ ML load skipped:", e)
        model = None
        vectorizer = None


# =============================
# 🔹 TEXT CLEANING
# =============================

def clean_text(text):
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# =============================
# 🔹 PREDICTION (SAFE)
# =============================

def predict_rating(synopsis: str):
    # 🚨 If ML not available (Render)
    if not TORCH_AVAILABLE or model is None or vectorizer is None:
        return None

    cleaned = clean_text(synopsis)
    vec = vectorizer.transform([cleaned]).toarray()
    tensor = torch.tensor(vec, dtype=torch.float32)

    with torch.no_grad():
        pred = model(tensor)

    return round(float(pred.item()), 2)


# =============================
# 🔹 LOCAL TEST
# =============================

if __name__ == "__main__":
    print(predict_rating("A gangster family fights for power in England"))
