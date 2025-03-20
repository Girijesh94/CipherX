#!/bin/bash

echo "Starting CipherX..."
python3 scripts/capture_packets.py
python3 scripts/preprocess_data.py
python3 scripts/block_threats.py
python3 app.py
