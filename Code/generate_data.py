# generate_data.py
import os
import time
import random
from datetime import datetime, timedelta
import pandas as pd

# --- Configuration ---
NUM_NODES = 50         # Number of nodes (or cells)
UPDATE_INTERVAL = 30   # seconds between updates
EXCEL_FILENAME = "synthetic_telecom_data.xlsx"

# --- Helper Function: Create a batch of data rows for the current timestamp ---
def generate_rows(current_time, num_nodes=NUM_NODES):
    rows = []
    for cell_id in range(1, num_nodes + 1):
        row = {
            "timestamp": current_time.strftime("%m/%d/%Y %H:%M:%S"),
            "cell_id": cell_id,
            "network_type": random.choice(["3G", "4G", "5G"]),
            "uplink_traffic_MB": round(random.uniform(5, 50), 2),
            "downlink_traffic_MB": round(random.uniform(10, 100), 2),
            "active_users": random.randint(10, 100),
            "call_drop_rate": round(random.uniform(0, 3), 2),
            "latency_ms": round(random.uniform(10, 100), 2),
            "throughput_Mbps": round(random.uniform(20, 120), 2),
            "signal_strength_dBm": round(random.uniform(-110, -70), 2),
            "resource_utilization": round(random.uniform(30, 100), 2),
            "handover_success_rate": round(random.uniform(80, 100), 2),
            "packet_loss_rate": round(random.uniform(0, 2), 2),
            "jitter_ms": round(random.uniform(0, 10), 2)
        }
        rows.append(row)
    return rows

# --- Load Existing Data (if available) ---
if os.path.exists(EXCEL_FILENAME):
    try:
        df_existing = pd.read_excel(EXCEL_FILENAME)
        print(f"Loaded existing file '{EXCEL_FILENAME}' with {len(df_existing)} rows.")
    except Exception as e:
        print(f"Error loading file: {e}")
        df_existing = pd.DataFrame()
else:
    df_existing = pd.DataFrame()

# --- Main Loop: Append new data every UPDATE_INTERVAL seconds ---
print("Starting data generation. Press Ctrl+C to stop.")
current_time = datetime.now()

while True:
    # Generate new batch for current timestamp
    new_rows = generate_rows(current_time)
    df_new = pd.DataFrame(new_rows)
    
    # Combine with any previously written data
    df_existing = pd.concat([df_existing, df_new], ignore_index=True)
    
    # Write the updated DataFrame to Excel (using openpyxl as the engine)
    try:
        df_existing.to_excel(EXCEL_FILENAME, index=False, engine="openpyxl")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Appended data for timestamp: {current_time.strftime('%m/%d/%Y %H:%M:%S')}")
    except Exception as e:
        print(f"Error writing to Excel: {e}")

    # Increment simulated time and wait for next update
    current_time += timedelta(seconds=UPDATE_INTERVAL)
    time.sleep(UPDATE_INTERVAL)
