import joblib
import pandas as pd

MODEL_FILE = "ml/models/rf_model.pkl"
FEATURE_FILE = "ml/models/feature_columns.pkl"

# Load model & feature order
model = joblib.load(MODEL_FILE)
feature_columns = joblib.load(FEATURE_FILE)

def predict_realtime(features_dict):
    """
    Predict real-time traffic behavior using trained ML model
    """

    if features_dict is None:
        return {
            "prediction": "NO_TRAFFIC",
            "attack_probability": 0.0,
            "benign_probability": 100.0
        }

    # Convert to DataFrame
    df = pd.DataFrame([features_dict])

    # Ensure correct feature order
    df = df.reindex(columns=feature_columns, fill_value=0)

    # Predict probabilities
    probs = model.predict_proba(df)[0]

    benign_prob = float(probs[0]) * 100
    attack_prob = float(probs[1]) * 100

    prediction = "MALICIOUS" if attack_prob >= 50 else "BENIGN"

    return {
        "prediction": prediction,
        "attack_probability": round(attack_prob, 2),
        "benign_probability": round(benign_prob, 2)
    }
