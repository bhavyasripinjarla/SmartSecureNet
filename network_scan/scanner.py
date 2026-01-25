import subprocess
import re

def scan_wifi_networks():
    try:
        command = ["netsh", "wlan", "show", "networks", "mode=bssid"]
        output = subprocess.check_output(
            command,
            shell=True,
            encoding="utf-8",
            errors="ignore"
        )

    except subprocess.CalledProcessError:
        return [{
            "ssid": "Wi-Fi Disabled / No Adapter",
            "bssid": None,
            "signal": None,
            "encryption": None,
            "risk": "HIGH",
            "warning": "Turn ON Wi-Fi"
        }]

    networks = []
    current = {}

    for line in output.splitlines():
        line = line.strip()

        # SSID
        if line.startswith("SSID"):
            if current:
                networks.append(current)

            current = {
                "ssid": line.split(":", 1)[1].strip(),
                "bssid": None,
                "signal": None,
                "encryption": "Unknown",
                "risk": "UNKNOWN"
            }

        # BSSID (MAC Address)
        elif line.startswith("BSSID"):
            current["bssid"] = line.split(":", 1)[1].strip()

        # Signal strength
        elif "Signal" in line:
            signal_str = line.split(":", 1)[1].strip().replace("%", "")
            current["signal"] = int(signal_str)

        # Encryption type
        elif "Authentication" in line:
            enc = line.split(":", 1)[1].strip()
            current["encryption"] = enc

            # Simple risk rules
            if enc.lower() in ["open", "none"]:
                current["risk"] = "HIGH"
            elif "WEP" in enc:
                current["risk"] = "MEDIUM"
            else:
                current["risk"] = "LOW"

    if current:
        networks.append(current)

    return networks
