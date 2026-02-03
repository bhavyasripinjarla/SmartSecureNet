import random

def extract_realtime_features(duration=10):
    """
    Simulates real-time packet behaviour features
    (In real systems this comes from tshark / pcap)
    """

    features = {
        "flow_duration": random.uniform(1, duration),
        "packet_rate": random.uniform(10, 200),
        "avg_packet_size": random.uniform(200, 1500),
        "syn_flag_count": random.randint(0, 10),
        "rst_flag_count": random.randint(0, 5),
    }

    return features
