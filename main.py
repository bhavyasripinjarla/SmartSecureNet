from network_scan.scanner import scan_wifi_networks
from packet_monitor.real_sniffer import capture_real_packets
from ml.realtime_feature_extractor import extract_flow_features
from ml.realtime_detector import predict_realtime
from ml.attack_simulator import simulate_attack_flow
from blockchain.trust_chain import get_trust_score, update_trust_score
from alerts.notifier import notify_user
from vpn_manager.vpn_trigger import trigger_vpn
from ui.dashboard import start_dashboard


# ============================
# CONFIGURATION
# ============================
USE_ATTACK_SIMULATION = False   # 🔁 Set True for demo attack
PACKET_CAPTURE_TIME = 10        # seconds


def run_security_engine():
    print("\n🔐 SmartSecureNet – Intelligent Public Wi-Fi Protection (ML-Based)\n")

    networks = scan_wifi_networks()

    for net in networks:
        print("=" * 70)

        ssid = net.get("ssid")

        print(f"📶 SSID        : {ssid}")
        print(f"📡 Signal      : {net.get('signal')}%")
        print(f"🔐 Encryption  : {net.get('encryption')}")

        # 1️⃣ Get current blockchain trust score
        trust_info = get_trust_score(ssid)
        print(f"🔗 Current Trust Score : {trust_info['trust_score']}/100")

        # 2️⃣ Feature extraction
        if USE_ATTACK_SIMULATION:
            print("\n🚨 DEMO MODE ENABLED – Simulating attack traffic")
            features = simulate_attack_flow()
        else:
            print(f"\n📡 Capturing real packets for {PACKET_CAPTURE_TIME} seconds...")
            packet_stats = capture_real_packets(duration=PACKET_CAPTURE_TIME)
            features = extract_flow_features(packet_stats)

        # 3️⃣ ML prediction
        ml_result = predict_realtime(features)

        print("\n🤖 ML Analysis Result")
        print("Prediction         :", ml_result["prediction"])
        print("Benign Probability :", ml_result["benign_probability"], "%")
        print("Attack Probability :", ml_result["attack_probability"], "%")

        # 4️⃣ Update blockchain trust score
        updated = update_trust_score(ssid, ml_result["attack_probability"])

        print("\n🔄 Blockchain Trust Update")
        print("Updated Trust Score:", updated["trust_score"], "/100")

        # 5️⃣ Response actions
        if ml_result["attack_probability"] > 80:
            print("\n🚨 HIGH RISK NETWORK DETECTED 🚨")
            notify_user(ssid, ml_result)
            trigger_vpn()

        elif ml_result["attack_probability"] > 50:
            print("\n⚠️ Suspicious network behavior detected")

        else:
            print("\n✅ Network behavior appears normal")

    print("\n🛡️ SmartSecureNet scan completed successfully.\n")


def main():
    print("==============================================")
    print("   SmartSecureNet – Security System Launcher   ")
    print("==============================================")
    print("1️⃣  Run Security Engine (CLI)")
    print("2️⃣  Launch Live Dashboard (Web UI)")
    print("3️⃣  Run BOTH (Recommended)")
    print("==============================================")

    choice = input("Enter your choice (1 / 2 / 3): ").strip()

    if choice == "1":
        run_security_engine()

    elif choice == "2":
        start_dashboard()

    elif choice == "3":
        run_security_engine()
        print("\n🌐 Launching Dashboard...\n")
        start_dashboard()

    else:
        print("❌ Invalid choice. Please restart and choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
