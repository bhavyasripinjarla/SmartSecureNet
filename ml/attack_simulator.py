import random

def simulate_attack_flow():
    """
    Generates flow features resembling malicious traffic
    (DDoS / DNS spoof / scanning behavior)
    """

    return {
        "flow_duration": random.randint(1, 10),
        "total_fwd_packets": random.randint(200, 500),
        "total_bwd_packets": random.randint(0, 10),
        "flow_packets_per_sec": random.uniform(1000, 5000),
        "packet_length_mean": random.uniform(50, 90),
        "packet_length_std": random.uniform(200, 500),
        "flow_iat_mean": random.uniform(0.0001, 0.01),
        "fwd_iat_mean": random.uniform(0.0001, 0.01),
        "bwd_iat_mean": random.uniform(0.1, 1.0),
        "avg_packet_size": random.uniform(60, 120)
    }
