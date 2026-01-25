import json
import os

CHAIN_FILE = "blockchain/trust_ledger.json"

# Initialize ledger if not exists
if not os.path.exists(CHAIN_FILE):
    with open(CHAIN_FILE, "w") as f:
        json.dump({}, f, indent=4)

def get_trust_score(ssid):
    with open(CHAIN_FILE, "r") as f:
        ledger = json.load(f)

    if ssid not in ledger:
        # Default trust score
        ledger[ssid] = {
            "trust_score": 80,
            "history": []
        }
        save_ledger(ledger)

    return ledger[ssid]

def update_trust_score(ssid, attack_probability):
    with open(CHAIN_FILE, "r") as f:
        ledger = json.load(f)

    if ssid not in ledger:
        ledger[ssid] = {
            "trust_score": 80,
            "history": []
        }

    score = ledger[ssid]["trust_score"]

    # Trust score adjustment logic
    if attack_probability < 20:
        delta = 2
    elif attack_probability < 50:
        delta = 0
    elif attack_probability < 80:
        delta = -5
    else:
        delta = -10

    new_score = max(0, min(100, score + delta))

    ledger[ssid]["trust_score"] = new_score
    ledger[ssid]["history"].append({
        "attack_probability": attack_probability,
        "delta": delta,
        "new_score": new_score
    })

    save_ledger(ledger)

    return ledger[ssid]

def save_ledger(ledger):
    with open(CHAIN_FILE, "w") as f:
        json.dump(ledger, f, indent=4)
