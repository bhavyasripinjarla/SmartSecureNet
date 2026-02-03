import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

DATA_PATH = "ml/data/cicids2017_selected.csv"
MODEL_PATH = "ml/models/rf_model.pkl"
FEATURES_PATH = "ml/models/feature_columns.pkl"

print("\n📊 Loading dataset...")
df = pd.read_csv(DATA_PATH)

# Load features used during training
features = joblib.load(FEATURES_PATH)

print("🧹 Cleaning data (handling inf / NaN values)...")
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(subset=features + ["Label"], inplace=True)

print(f"✅ Cleaned dataset size: {df.shape[0]} rows")

# 🔑 CRITICAL FIX: Label encoding
print("🔁 Encoding labels...")
df["Label"] = df["Label"].apply(lambda x: 0 if x == "BENIGN" else 1)

X = df[features]
y = df["Label"]

print("\n🤖 Loading trained model...")
model = joblib.load(MODEL_PATH)

print("🔍 Running predictions...")
y_pred = model.predict(X)

print("\n✅ MODEL EVALUATION RESULTS")
print("===================================")
print(f"Accuracy : {accuracy_score(y, y_pred) * 100:.2f} %\n")

print("Classification Report:")
print(classification_report(y, y_pred, target_names=["BENIGN", "ATTACK"]))

print("Confusion Matrix:")
print(confusion_matrix(y, y_pred))
