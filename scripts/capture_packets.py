from scapy.all import sniff, wrpcap

def capture_packets(interface="Wi-Fi", packet_count=100):
    packets = sniff(iface=interface, count=packet_count)
    wrpcap("data/raw_data.pcapng", packets)
    print(f"Captured {packet_count} packets and saved to data/raw_data.pcapng")

if __name__ == "__main__":
    capture_packets()
