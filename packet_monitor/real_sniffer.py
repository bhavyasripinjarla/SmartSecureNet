import subprocess
import time

def capture_real_packets(duration=10, interface="Wi-Fi"):
    """
    Capture real packets using tshark and return basic stats
    """
    print(f"📡 Capturing real packets for {duration} seconds...")

    cmd = [
        "tshark",
        "-i", interface,
        "-a", f"duration:{duration}",
        "-T", "fields",
        "-e", "frame.len",
        "-e", "arp.opcode",
        "-e", "dns.qry.name"
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

    packet_sizes = []
    arp_count = 0
    dns_count = 0

    for line in process.stdout:
        fields = line.strip().split("\t")

        if fields[0]:
            packet_sizes.append(int(fields[0]))

        if len(fields) > 1 and fields[1]:
            arp_count += 1

        if len(fields) > 2 and fields[2]:
            dns_count += 1

    total_packets = len(packet_sizes)
    total_bytes = sum(packet_sizes)

    return {
        "duration": duration,
        "total_packets": total_packets,
        "total_bytes": total_bytes,
        "packet_sizes": packet_sizes,
        "arp_count": arp_count,
        "dns_count": dns_count
    }
