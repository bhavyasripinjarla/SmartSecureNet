import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

DATA_FILE = "data/cicids2017_labeled.csv"
MODEL_DIR = "models"

# Create model directory if not exists
os.makedirs(MODEL_DIR, exist_ok=True)

def train_rf():
    print("Loading dataset...")
    df = pd.read_csv(DATA_FILE, low_memory=False)

    # Separate features and label
    X = df.drop(columns=["Label"])
    y = df["Label"]

    print(f"Total samples: {len(df)}")
    print(f"Features used: {len(X.columns)}")

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("Training Random Forest model...")

    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        n_jobs=-1,
        random_state=42,
        class_weight="balanced"
    )

    rf.fit(X_train, y_train)

    print("Model training completed")

    # Evaluation
    y_pred = rf.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    print("\nModel Accuracy:", round(acc * 100, 2), "%")

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Save model & feature names
    joblib.dump(rf, f"{MODEL_DIR}/rf_model.pkl")
    joblib.dump(list(X.columns), f"{MODEL_DIR}/feature_columns.pkl")

    print("\nModel saved successfully:")
    print(" - models/rf_model.pkl")
    print(" - models/feature_columns.pkl")

if __name__ == "__main__":
    train_rf()
