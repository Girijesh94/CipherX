import pandas as pd
import os

# Load filtered data
df = pd.read_csv("data/filtered_data.csv")
anomalies = df[df["is_anomaly"] == -1]["src_ip"].unique()

def block_ip(ip):
    if os.name == "nt":  # Windows
        os.system(f"netsh advfirewall firewall add rule name=\"Block {ip}\" dir=in action=block remoteip={ip}")
    else:  # Linux/macOS
        os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")

for ip in anomalies:
    print(f"Blocking IP: {ip}")
    block_ip(ip)

print("Threat blocking complete.")
