from ml.realtime_detector import analyze_realtime_packets

print("\n🧪 ML VERIFICATION TEST\n")

result = analyze_realtime_packets(duration=10)

print("\n🔍 ML Verdict")
print(f"Prediction           : {result['prediction']}")
print(f"Benign Probability   : {result['benign_prob']} %")
print(f"Attack Probability   : {result['attack_prob']} %")
