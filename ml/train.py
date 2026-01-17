import os
import sys
import django
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

# 🔹 Setup Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from ml.features import prepare_features

# 🔹 Load & prepare data
df = prepare_features()

X_text = df["clean_synopsis"].fillna("")

# 🔹 Ensure rating is numeric
y = pd.to_numeric(df["rating"], errors="coerce").values

mask = ~pd.isna(y)
X_text = X_text[mask]
y = y[mask]


# 🔹 Convert text → numbers
vectorizer = TfidfVectorizer(
    max_features=1000,
    stop_words="english"
)

X = vectorizer.fit_transform(X_text).toarray()

# 🔹 Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 🔹 Convert to tensors
X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
y_test = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)


# 🔹 Define model (ONLY architecture)
class RatingPredictor(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=0.5)
        self.fc2 = nn.Linear(64, 1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x


# 🔹 Initialize model
model = RatingPredictor(X_train.shape[1])
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)  # ✅ stable LR


# 🔹 Training loop
for epoch in range(300):
    preds = model(X_train)
    loss = criterion(preds, y_train)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 50 == 0:
        print(f"Epoch {epoch} | Train Loss: {loss.item():.4f}")


# 🔹 Evaluation
with torch.no_grad():
    test_preds = model(X_test)
    test_loss = criterion(test_preds, y_test)
    print("\nTest Loss:", test_loss.item())


# 🔹 Sample predictions
print("\nSample Predictions:")
for i in range(len(test_preds)):
    print(f"Predicted: {test_preds[i].item():.2f} | Actual: {y_test[i].item():.2f}")


# 🔹 Save trained model
os.makedirs("ml/models", exist_ok=True)
torch.save(model.state_dict(), "ml/models/rating_model.pt")

# 🔹 Save vectorizer
import pickle
with open("ml/models/tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("\n✅ Model and vectorizer saved successfully!")
