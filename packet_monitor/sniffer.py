def start_packet_capture(packet_limit=20):
    """
    Windows-safe simulated packet capture
    Returns packets + counters
    """

    packets = [
        # ARP spoofing simulation
        {"src_ip": "192.168.1.1", "src_mac": "AA:BB:CC:01", "is_arp": True},
        {"src_ip": "192.168.1.1", "src_mac": "AA:BB:CC:02", "is_arp": True},

        # DNS spoofing simulation
        {"dns_query": "secure-bank.com", "dst_ip": "10.0.0.5", "is_dns": True},
        {"dns_query": "secure-bank.com", "dst_ip": "10.0.0.9", "is_dns": True},

        # Normal traffic
        {"src_ip": "192.168.1.5"},
        {"src_ip": "192.168.1.10"},
    ]

    total_packets = len(packets)
    arp_anomalies = sum(1 for p in packets if p.get("is_arp"))
    dns_anomalies = sum(1 for p in packets if p.get("is_dns"))

    return {
        "packets": packets,
        "total_packets": total_packets,
        "arp_anomalies": arp_anomalies,
        "dns_anomalies": dns_anomalies
    }
