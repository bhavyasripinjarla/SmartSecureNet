import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    roc_auc_score
)

DATA_FILE = "data/cicids2017_labeled.csv"
MODEL_FILE = "models/rf_model.pkl"

def evaluate_model():
    print("Loading dataset...")
    df = pd.read_csv(DATA_FILE, low_memory=False)

    X = df.drop(columns=["Label"])
    y = df["Label"]

    # Same split as training
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("Loading trained model...")
    model = joblib.load(MODEL_FILE)

    print("Running predictions...")
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)

    print("\nConfusion Matrix:")
    print(cm)

    # Classification Report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # ROC-AUC Score
    roc_auc = roc_auc_score(y_test, y_prob)
    print(f"ROC-AUC Score: {round(roc_auc, 4)}")

if __name__ == "__main__":
    evaluate_model()
