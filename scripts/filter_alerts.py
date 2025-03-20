from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import os

# Get correct dataset path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Script directory
file_path = os.path.join(BASE_DIR, "..", "data", "network_data.csv")  # Data folder

# Load dataset
try:
    df = pd.read_csv(file_path)
    print(f"✅ Dataset loaded successfully! Columns: {df.columns.tolist()}")
except FileNotFoundError:
    print(f"❌ Error: File not found at {file_path}")
    exit()

# Encode categorical columns
categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
encoder = LabelEncoder()

for col in categorical_columns:
    df[col] = encoder.fit_transform(df[col])

# Select feature columns (excluding non-relevant ones)
exclude_columns = ["src_ip", "dst_ip", "info"]
feature_columns = [col for col in df.columns if col not in exclude_columns]

# Train Isolation Forest
anomaly_detector = IsolationForest(n_estimators=50, contamination=0.05, random_state=42)
anomaly_detector.fit(df[feature_columns])

# Predict anomalies
df["anomaly_score"] = anomaly_detector.decision_function(df[feature_columns])
df["is_anomaly"] = anomaly_detector.predict(df[feature_columns])  # -1 (anomaly), 1 (normal)

# Save filtered results
output_path = os.path.join(BASE_DIR, "..", "data", "filtered_data.csv")
df.to_csv(output_path, index=False)

print(f"✅ False alerts filtered and saved successfully at {output_path}! 🚀")
