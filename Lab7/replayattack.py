from scapy.all import *

# Read the captured packets
packets = rdpcap("captured.pcap")

# Replay the packets to localhost
sendp(packets, iface="lo")
