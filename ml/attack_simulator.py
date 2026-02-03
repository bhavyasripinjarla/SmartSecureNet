# ml/attack_simulator.py

def generate_attack_features():
    """
    CICIDS2017-style STRONG ATTACK
    """
    return {
        "Flow Duration": 5,
        "Total Fwd Packets": 50000,
        "Total Backward Packets": 45000,
        "Flow Packets/s": 30000,
        "Packet Length Mean": 1400,
        "Packet Length Std": 1000,
        "Flow IAT Mean": 0.01,
        "Flow IAT Std": 0.005,
        "Fwd IAT Mean": 0.01,
        "Bwd IAT Mean": 0.01,
        "Average Packet Size": 1300
    }


def generate_benign_features():
    """
    Normal browsing traffic
    """
    return {
        "Flow Duration": 200000,
        "Total Fwd Packets": 120,
        "Total Backward Packets": 110,
        "Flow Packets/s": 2,
        "Packet Length Mean": 500,
        "Packet Length Std": 80,
        "Flow IAT Mean": 400,
        "Flow IAT Std": 120,
        "Fwd IAT Mean": 380,
        "Bwd IAT Mean": 390,
        "Average Packet Size": 520
    }
