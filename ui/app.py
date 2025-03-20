from flask import Flask, render_template
import pandas as pd
import sys
import os

# ✅ Ensure 'scripts' is in Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.ip_mapping import ip_map   # Correct import
  # Now it should work!
  # Correct import
  # Import IP mapping dictionary

app = Flask(__name__)

protocol_map = {
    0: "ICMP",
    1: "TCP",
    2: "UDP"
}

def load_data():
    df = pd.read_csv("data/filtered_data.csv")

    # Convert numeric IPs to actual IPs
    df["src_ip"] = df["src_ip"].map(ip_map)
    df["dst_ip"] = df["dst_ip"].map(ip_map)
    
    df["protocol"] = df["protocol"].map(protocol_map)

    # Define risk levels based on anomaly score
    def get_risk_level(score):
        if score > 0.5:
            return "🔴 High Risk"
        elif score > 0.2:
            return "🟠 Medium Risk"
        else:
            return "✅ Normal"

    df["risk_level"] = df["anomaly_score"].apply(get_risk_level)

    return df[["src_ip", "dst_ip", "protocol", "anomaly_score", "risk_level"]]

@app.route("/")
def index():
    data = load_data().to_dict(orient="records")
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
