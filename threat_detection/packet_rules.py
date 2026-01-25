from collections import defaultdict

def detect_arp_spoofing(packets):
    """
    Detects ARP spoofing by checking
    multiple MACs claiming same IP
    """
    ip_mac_map = defaultdict(set)

    for pkt in packets:
        if pkt.get("is_arp") and pkt.get("src_ip") and pkt.get("src_mac"):
            ip_mac_map[pkt["src_ip"]].add(pkt["src_mac"])

    for ip, macs in ip_mac_map.items():
        if len(macs) > 1:
            return True, f"ARP spoofing detected for IP {ip}"

    return False, None


def detect_dns_spoofing(packets):
    """
    Detects suspicious DNS behavior
    """
    dns_queries = defaultdict(set)

    for pkt in packets:
        if pkt.get("is_dns") and pkt.get("dns_query") and pkt.get("dst_ip"):
            dns_queries[pkt["dns_query"]].add(pkt["dst_ip"])

    for domain, ips in dns_queries.items():
        if len(ips) > 2:
            return True, f"Possible DNS spoofing for domain {domain}"

    return False, None
