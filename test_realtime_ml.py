from ml.attack_simulator import simulate_attack_flow
from ml.realtime_detector import predict_realtime

print("\n🚨 Simulating Attack Traffic...\n")

features = simulate_attack_flow()

result = predict_realtime(features)

print("🔍 ML Verdict")
print("Prediction           :", result["prediction"])
print("Benign Probability   :", result["benign_probability"], "%")
print("Attack Probability   :", result["attack_probability"], "%")
