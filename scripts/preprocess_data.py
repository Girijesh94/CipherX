import pyshark
import pandas as pd

def extract_features(pcap_file):
    cap = pyshark.FileCapture(pcap_file)
    data = []
    
    for packet in cap:
        try:
            data.append({
                "src_ip": packet.ip.src,
                "dst_ip": packet.ip.dst,
                "protocol": packet.transport_layer,
                "length": packet.length,
                "info": str(packet.highest_layer)
            })
        except AttributeError:
            continue

    df = pd.DataFrame(data)
    df.to_csv("data/network_data.csv", index=False)
    print("Converted .pcapng to CSV.")

if __name__ == "__main__":
    extract_features("data/raw_data.pcapng")
