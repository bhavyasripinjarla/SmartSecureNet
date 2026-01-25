# Common keywords used in fake / evil twin Wi-Fi names
SUSPICIOUS_SSID_KEYWORDS = [
    "free", "public", "open", "wifi", "airport", "cafe", "mall"
]

def assess_network_risk(network):
    """
    Assess risk level of a Wi-Fi network using rule-based logic
    """
    ssid = network.get("ssid", "").lower()
    signal = network.get("signal", 0)
    encryption = network.get("encryption", "").lower()

    risk_score = 0
    reasons = []

    # Rule 1: Open or unsecured Wi-Fi
    if encryption in ["open", "none", ""]:
        risk_score += 3
        reasons.append("Open or unsecured Wi-Fi network")

    # Rule 2: Weak signal strength (possible rogue AP)
    if signal is not None and signal < 40:
        risk_score += 2
        reasons.append("Weak signal strength")

    # Rule 3: Suspicious SSID naming
    for keyword in SUSPICIOUS_SSID_KEYWORDS:
        if keyword in ssid:
            risk_score += 1
            reasons.append("Suspicious SSID naming pattern")
            break

    # Risk classification
    if risk_score >= 5:
        risk_level = "HIGH"
    elif risk_score >= 3:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "reasons": reasons
    }
from threat_detection.packet_rules import (
    detect_arp_spoofing,
    detect_dns_spoofing
)

def assess_packet_threats(packets):
    """
    Packet-level threat assessment
    """
    threats = []

    arp_attack, arp_reason = detect_arp_spoofing(packets)
    if arp_attack:
        threats.append(("HIGH", arp_reason))

    dns_attack, dns_reason = detect_dns_spoofing(packets)
    if dns_attack:
        threats.append(("MEDIUM", dns_reason))

    if threats:
        highest = max(threats, key=lambda x: x[0])
        return {
            "packet_threat": True,
            "risk_level": highest[0],
            "reasons": [t[1] for t in threats]
        }

    return {
        "packet_threat": False,
        "risk_level": "LOW",
        "reasons": []
    }
