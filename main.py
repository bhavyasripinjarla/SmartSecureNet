from network_scan.scanner import scan_wifi_networks
from network_scan.connected_wifi import get_connected_ssid
from ml.realtime_detector import analyze_realtime_packets
from alerts.notifier import notify_user
from vpn_manager.vpn_trigger import trigger_vpn
from blockchain.trust_chain import get_trust_score, update_trust_score
from ui.dashboard import start_dashboard


def run_security_engine():
    print("\n🔐 SmartSecureNet – Intelligent Public Wi-Fi Protection (ML-Based)\n")

    connected_ssid = get_connected_ssid()
    networks = scan_wifi_networks()

    print(f"📡 Connected Wi-Fi : {connected_ssid}\n")

    for net in networks:
        print("=" * 70)

        ssid = net.get("ssid")
        signal = net.get("signal")
        encryption = net.get("encryption")

        print(f"📶 SSID        : {ssid}")
        print(f"📡 Signal      : {signal}%")
        print(f"🔐 Encryption  : {encryption}")

        trust_info = get_trust_score(ssid)
        print(f"🔗 Current Trust Score : {trust_info['trust_score']}/100")

        # 🔴 IMPORTANT FIX HERE
        if ssid != connected_ssid:
            print("\n📡 Packet analysis skipped (not connected)")
            final_risk = "LOW"

        else:
            print("\n📡 Capturing REAL packet behaviour...")
            ml_result = analyze_realtime_packets(duration=10)

            prediction = ml_result["prediction"]
            benign_prob = ml_result["benign_prob"]
            attack_prob = ml_result["attack_prob"]

            print("\n🤖 ML Analysis Result")
            print(f"Prediction         : {prediction}")
            print(f"Benign Probability : {benign_prob:.2f} %")
            print(f"Attack Probability : {attack_prob:.2f} %")

            if prediction == "ATTACK" or attack_prob >= 50:
                final_risk = "HIGH"
            elif attack_prob >= 30:
                final_risk = "MEDIUM"
            else:
                final_risk = "LOW"

            if final_risk == "HIGH":
                print("\n🚨 MALICIOUS NETWORK BEHAVIOUR DETECTED 🚨")
                notify_user(ssid, ml_result)
                trigger_vpn()
            elif final_risk == "MEDIUM":
                print("\n⚠️ Suspicious activity detected. Monitoring advised.")
            else:
                print("\n✅ Network behaviour appears normal")

        updated = update_trust_score(ssid, final_risk)
        print("\n🔄 Blockchain Trust Update")
        print(f"Updated Trust Score: {updated['trust_score']} /100")

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
        print("❌ Invalid choice.")


if __name__ == "__main__":
    main()
