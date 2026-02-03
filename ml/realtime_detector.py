import joblib
import numpy as np
import pandas as pd
from ml.realtime_feature_extractor import extract_realtime_features

MODEL_PATH = "ml/models/rf_model.pkl"
FEATURES_PATH = "ml/models/feature_columns.pkl"

# Load model and feature schema
model = joblib.load(MODEL_PATH)
feature_columns = joblib.load(FEATURES_PATH)

def analyze_realtime_packets(duration=10):
    """
    Extracts real-time behaviour and aligns it with trained feature space
    """

    print(f"📡 Capturing REAL packet behaviour for {duration} seconds...")

    realtime_features = extract_realtime_features(duration)

    # Create empty feature row with ALL expected columns
    feature_row = {col: 0 for col in feature_columns}

    # Map available real-time features to training features
    feature_mapping = {
        "flow_duration": "Flow Duration",
        "packet_rate": "Flow Packets/s",
        "avg_packet_size": "Average Packet Size",
        "syn_flag_count": "SYN Flag Count",
        "rst_flag_count": "RST Flag Count"
    }

    for rt_key, train_key in feature_mapping.items():
        if train_key in feature_row:
            feature_row[train_key] = realtime_features.get(rt_key, 0)

    # Convert to DataFrame (IMPORTANT)
    X = pd.DataFrame([feature_row])

    # Predict
    probabilities = model.predict_proba(X)[0]

    benign_prob = probabilities[0] * 100
    attack_prob = probabilities[1] * 100

    prediction = "ATTACK" if attack_prob >= 50 else "BENIGN"

    return {
        "prediction": prediction,
        "benign_prob": round(benign_prob, 2),
        "attack_prob": round(attack_prob, 2)
    }
