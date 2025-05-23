from scapy.all import rdpcap, raw

def detect_replay(pcap_file):
    packets = rdpcap(pcap_file)
    seen = {}  # Dictionary to track seen packets
    found_replay = False

    print(f"Analyzing {pcap_file} for replay attacks...")

    for i, pkt in enumerate(packets):
        try:
            if pkt.haslayer("IP"):  # Ensure it's an IP packet
                key = (pkt["IP"].src, pkt["IP"].dst, raw(pkt["IP"].payload))  # Use raw() for hashable payload
            
                if key in seen:
                    seen[key] += 1
                    print(f"⚠️ Replay detected: Packet {i} (Count: {seen[key]})")
                    found_replay = True
                else:
                    seen[key] = 1
        except Exception as e:
            print(f"Skipping packet {i}: {e}")

    if not found_replay:
        print("No replay attack detected.")

if __name__ == "__main__":
    detect_replay("afterreplaycapture.pcap")
