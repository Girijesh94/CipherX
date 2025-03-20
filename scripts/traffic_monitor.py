from scapy.all import sniff, IP
import pandas as pd
import time
from collections import defaultdict

# Store request counts
request_counts = defaultdict(int)
traffic_data = []

# Parameters for DDoS detection
TIME_WINDOW = 10  # seconds
THRESHOLD = 50    # max allowed requests per IP in TIME_WINDOW

def process_packet(packet):
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        protocol = packet[IP].proto

        # Track request counts
        request_counts[src_ip] += 1

        # Store packet data
        traffic_data.append({"src_ip": src_ip, "dst_ip": dst_ip, "protocol": protocol, "timestamp": time.time()})

        # Check for potential DDoS attack
        if request_counts[src_ip] > THRESHOLD:
            print(f"🚨 DDoS Detected from {src_ip}! Blocking...")
            block_ip(src_ip)

# Function to block an IP using iptables (Linux)
def block_ip(ip):
    import os
    os.system(f"iptables -A INPUT -s {ip} -j DROP")
    print(f"❌ Blocked IP: {ip}")

# Start sniffing packets
def start_sniffing(interface="eth0", count=100):
    print("[🔍] Monitoring Network Traffic...")
    sniff(iface=interface, prn=process_packet, count=count, store=False)

    # Save captured data
    df = pd.DataFrame(traffic_data)
    df.to_csv("data/live_traffic.csv", index=False)
    print("[✅] Traffic data saved!")

if __name__ == "__main__":
    start_sniffing()
