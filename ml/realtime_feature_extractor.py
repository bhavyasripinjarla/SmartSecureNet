import numpy as np

def extract_flow_features(packet_stats):
    duration = packet_stats["duration"]
    packets = packet_stats["total_packets"]
    bytes_ = packet_stats["total_bytes"]
    sizes = packet_stats["packet_sizes"]

    if packets == 0:
        return None

    features = {
        "Flow Duration": duration * 1_000_000,  # microseconds
        "Total Fwd Packets": packets,
        "Total Backward Packets": 0,
        "Flow Bytes/s": bytes_ / duration,
        "Flow Packets/s": packets / duration,
        "Packet Length Mean": np.mean(sizes),
        "Packet Length Std": np.std(sizes),
        "Packet Length Variance": np.var(sizes),
        "Flow IAT Mean": duration / packets,
        "Flow IAT Std": 0,
        "Fwd IAT Mean": duration / packets,
        "Bwd IAT Mean": 0,
        "Fwd Header Length": 0,
        "Bwd Header Length": 0,
        "Average Packet Size": np.mean(sizes),
        "Active Mean": duration,
        "Idle Mean": 0
    }

    return features
