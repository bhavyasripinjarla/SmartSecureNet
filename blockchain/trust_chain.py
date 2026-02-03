import json
import os

LEDGER_FILE = "blockchain/trust_ledger.json"


def load_ledger():
    if not os.path.exists(LEDGER_FILE):
        return {}
    with open(LEDGER_FILE, "r") as f:
        return json.load(f)


def save_ledger(data):
    with open(LEDGER_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_trust_score(ssid):
    ledger = load_ledger()

    if ssid not in ledger:
        ledger[ssid] = {
            "trust_score": 80,
            "history": [80]
        }
        save_ledger(ledger)

    return ledger[ssid]


def update_trust_score(ssid, risk_level):
    ledger = load_ledger()

    if ssid not in ledger:
        ledger[ssid] = {
            "trust_score": 80,
            "history": []
        }

    current_score = ledger[ssid]["trust_score"]

    # 🔑 Trust update logic based on FINAL RISK
    if risk_level == "LOW":
        current_score = min(100, current_score + 2)
    elif risk_level == "MEDIUM":
        current_score = max(0, current_score - 5)
    elif risk_level == "HIGH":
        current_score = max(0, current_score - 15)

    ledger[ssid]["trust_score"] = current_score
    ledger[ssid]["history"].append(current_score)

    save_ledger(ledger)

    return {
        "ssid": ssid,
        "trust_score": current_score,
        "risk_level": risk_level
    }
