import joblib
import pandas as pd

MODEL_PATH = "ml/models/rf_model.pkl"
FEATURES_PATH = "ml/models/feature_columns.pkl"

# Load model & feature list
model = joblib.load(MODEL_PATH)
feature_columns = joblib.load(FEATURES_PATH)

def test_sample(sample_name, feature_values):
    df = pd.DataFrame([feature_values], columns=feature_columns)
    probs = model.predict_proba(df)[0]

    print(f"\n🧪 TEST CASE: {sample_name}")
    print(f"Benign Probability : {probs[0]*100:.2f}%")
    print(f"Attack Probability : {probs[1]*100:.2f}%")
    print("Prediction         :", "ATTACK" if probs[1] > 0.5 else "BENIGN")


# 🟢 Clearly BENIGN traffic
benign_sample = [10, 5, 2, 0.2, 0.1, 50, 20, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0]

# 🔴 Clearly ATTACK-like traffic
attack_sample = [10000, 9000, 200, 120, 95, 1500, 900, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1]

# 🟡 Borderline traffic
borderline_sample = [500, 400, 50, 10, 8, 300, 150, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1]

test_sample("BENIGN TRAFFIC", benign_sample)
test_sample("ATTACK TRAFFIC", attack_sample)
test_sample("BORDERLINE TRAFFIC", borderline_sample)
