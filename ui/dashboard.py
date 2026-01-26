from flask import Flask, render_template
from network_scan.scanner import scan_wifi_networks
from packet_monitor.real_sniffer import capture_real_packets
from ml.realtime_feature_extractor import extract_flow_features
from ml.realtime_detector import predict_realtime
from blockchain.trust_chain import get_trust_score
import json
from flask import Flask
app = Flask(__name__)

app = Flask(__name__, template_folder="templates")

LEDGER_FILE = "blockchain/trust_ledger.json"

def load_ledger():
    with open(LEDGER_FILE, "r") as f:
        return json.load(f)

@app.route("/")
def dashboard():
    networks = scan_wifi_networks()
    ledger = load_ledger()
    display_data = []

    for net in networks:
        ssid = net.get("ssid")

        # ML analysis
        packet_stats = capture_real_packets(duration=5)
        features = extract_flow_features(packet_stats)
        ml_result = predict_realtime(features)

        # Blockchain trust
        trust_info = get_trust_score(ssid)
        trust_score = trust_info["trust_score"]

        history = ledger.get(ssid, {}).get("history", [])
        score_history = [h["new_score"] for h in history]

        # Badge logic
        if trust_score >= 70:
            badge = "Trusted"
            badge_color = "green"
        elif trust_score >= 40:
            badge = "Caution"
            badge_color = "orange"
        else:
            badge = "Untrusted"
            badge_color = "red"

        display_data.append({
            "ssid": ssid,
            "signal": net.get("signal"),
            "encryption": net.get("encryption"),
            "prediction": ml_result["prediction"],
            "attack_prob": ml_result["attack_probability"],
            "benign_prob": ml_result["benign_probability"],
            "trust_score": trust_score,
            "badge": badge,
            "badge_color": badge_color,
            "score_history": score_history
        })

    return render_template("dashboard.html", networks=display_data)

def start_dashboard():
    print("🌐 Dashboard running at http://127.0.0.1:5000")
    app.run(debug=False)
def start_dashboard():
    app.run(debug=False)
