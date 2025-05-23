from scapy.all import rdpcap, raw
import time

LOG_FILE = "replay_log.txt"
TIME_WINDOW = 10  # Allowable time window (in seconds)

def log_suspicious_activity(packet_info):
    """Logs detected replay attacks to a file."""
    with open(LOG_FILE, "a") as log:
        log.write(f"{time.ctime()} - Replay Detected: {packet_info}\n")

def detect_and_prevent_replay(pcap_file):
    packets = rdpcap(pcap_file)
    seen = {}  # Dictionary to store (source, destination, payload) and their timestamps
    found_replay = False

    print(f"Analyzing {pcap_file} for replay attacks...")

    for i, pkt in enumerate(packets):
        try:
            if pkt.haslayer("IP"):
                key = (pkt["IP"].src, pkt["IP"].dst, raw(pkt["IP"].payload))  # Hashable tuple
                timestamp = pkt.time  # Capture the packet's timestamp

                if key in seen:
                    time_diff = timestamp - seen[key]  # Check time difference

                    if time_diff < TIME_WINDOW:
                        print(f"⚠️ Replay detected: Packet {i} (Time Diff: {time_diff:.2f}s)")
                        log_suspicious_activity(f"Packet {i} - {key} (Time Diff: {time_diff:.2f}s)")
                        found_replay = True
                else:
                    seen[key] = timestamp  # Store timestamp for first occurrence
        except Exception as e:
            print(f"Skipping packet {i}: {e}")

    if not found_replay:
        print("No replay attack detected.")

if __name__ == "__main__":
    detect_and_prevent_replay("capturedafterreplay1.pcap")
