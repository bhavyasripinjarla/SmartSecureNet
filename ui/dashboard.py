from flask import Flask, render_template
from network_scan.scanner import scan_wifi_networks
from network_scan.connected_wifi import get_connected_ssid
from blockchain.trust_chain import get_trust_score
from ml.realtime_detector import analyze_realtime_packets
import re

app = Flask(__name__)

# 🔧 Normalize SSID (fix emoji / encoding issues)
def normalize_ssid(ssid):
    if not ssid:
        return ""
    ssid = ssid.encode("ascii", "ignore").decode()
    return re.sub(r"\s+", "", ssid.lower())


@app.route("/")
def dashboard():
    networks = scan_wifi_networks()
    connected_ssid = get_connected_ssid()
    display_data = []

    for net in networks:
        ssid = net.get("ssid")

        trust_info = get_trust_score(ssid)
        trust_score = trust_info.get("trust_score", 50)

        # ✅ Ensure trust history is always a list
        score_history = trust_info.get("score_history")

# Ensure score_history is a valid list with at least 2 points
        if not isinstance(score_history, list) or len(score_history) < 2:
            score_history = [
            max(trust_score - 5, 0),
            trust_score
            ]

        # 🔐 Run ML ONLY for connected Wi-Fi
        if normalize_ssid(ssid) == normalize_ssid(connected_ssid):
            ml_result = analyze_realtime_packets(duration=5)

            prediction = ml_result["prediction"]
            attack_prob = round(ml_result["attack_prob"], 2)

            if attack_prob >= 50:
                badge = "HIGH RISK"
                badge_color = "red"
            elif attack_prob >= 30:
                badge = "MEDIUM RISK"
                badge_color = "orange"
            else:
                badge = "SAFE"
                badge_color = "green"

        else:
            prediction = "NOT CONNECTED"
            attack_prob = "N/A"
            badge = "UNKNOWN"
            badge_color = "orange"

        display_data.append({
            "ssid": ssid,
            "signal": net.get("signal"),
            "encryption": net.get("encryption"),
            "prediction": prediction,
            "attack_prob": attack_prob,
            "trust_score": trust_score,
            "badge": badge,
            "badge_color": badge_color,
            "score_history": score_history
        })

    return render_template(
        "dashboard.html",
        networks=display_data,
        cloud=False
    )


def start_dashboard():
    app.run(host="127.0.0.1", port=5000, debug=False)
