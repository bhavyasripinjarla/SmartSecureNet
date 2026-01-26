from flask import Flask, render_template
import os

from network_scan.scanner import scan_wifi_networks
from blockchain.trust_chain import get_trust_score
from ml.realtime_detector import analyze_realtime_packets

# ⚠️ Only import real sniffer for LOCAL use
if not os.environ.get("RENDER"):
    from packet_monitor.real_sniffer import capture_real_packets

app = Flask(__name__)

IS_CLOUD = os.environ.get("RENDER", False)


@app.route("/")
def dashboard():
    networks = scan_wifi_networks()
    display_data = []

    for net in networks:
        ssid = net.get("ssid")

        trust_info = get_trust_score(ssid)
        trust_score = trust_info["trust_score"]
        score_history = trust_info.get("history", [trust_score])

        # ----------------------------
        # CLOUD MODE (Simulated packets)
        # ----------------------------
        if IS_CLOUD:
            packet_stats = {
                "total_packets": 120,
                "arp_anomalies": 1,
                "dns_anomalies": 0
            }

            ml_result = {
                "prediction": "BENIGN",
                "attack_prob": 8
            }

        # ----------------------------
        # LOCAL MODE (Real packets)
        # ----------------------------
        else:
            packet_stats = capture_real_packets(duration=5)
            ml_result = analyze_realtime_packets(duration=5)

        # Badge logic
        if trust_score >= 80:
            badge = "TRUSTED"
            badge_color = "green"
        elif trust_score >= 50:
            badge = "SUSPICIOUS"
            badge_color = "orange"
        else:
            badge = "UNTRUSTED"
            badge_color = "red"

        display_data.append({
            "ssid": ssid,
            "signal": net.get("signal"),
            "encryption": net.get("encryption"),
            "prediction": ml_result["prediction"],
            "attack_prob": ml_result["attack_prob"],
            "trust_score": trust_score,
            "score_history": score_history,
            "badge": badge,
            "badge_color": badge_color,
            "total_packets": packet_stats["total_packets"],
            "arp": packet_stats["arp_anomalies"],
            "dns": packet_stats["dns_anomalies"]
        })

    return render_template("dashboard.html", networks=display_data, cloud=IS_CLOUD)


def start_dashboard():
    app.run(debug=False)
