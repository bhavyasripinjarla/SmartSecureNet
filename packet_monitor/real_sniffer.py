import subprocess
import time

def capture_real_packets(duration=10):
    """
    Capture real packets using tshark
    Returns basic packet statistics
    """

    cmd = [
        "tshark",
        "-i", "Wi-Fi",
        "-a", f"duration:{duration}",
        "-T", "fields",
        "-e", "frame.len"
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

    packet_lengths = []

    for line in process.stdout:
        try:
            packet_lengths.append(int(line.strip()))
        except:
            pass

    process.wait()

    return packet_lengths
