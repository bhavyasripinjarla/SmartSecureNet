from flask import Flask, request, jsonify
from ml.realtime_detector import predict_realtime
from blockchain.trust_chain import get_trust_score, update_trust_score

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json

    ssid = data["ssid"]
    features = data["features"]

    ml_result = predict_realtime(features)
    trust = update_trust_score(ssid, ml_result["attack_probability"])

    return jsonify({
        "prediction": ml_result["prediction"],
        "attack_probability": ml_result["attack_probability"],
        "benign_probability": ml_result["benign_probability"],
        "trust_score": trust["trust_score"]
    })

@app.route("/")
def home():
    return "SmartSecureNet Cloud API is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
