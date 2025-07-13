import time
import pandas as pd
from datetime import datetime
from arango import ArangoClient

# --- Configuration ---
EXCEL_FILENAME = "synthetic_telecom_data.xlsx"
UPDATE_INTERVAL = 30  # seconds
ARANGO_URL = "http://localhost:8529"
DB_NAME = "_system"   # using the _system database
USERNAME = "root"
PASSWORD = "yourpassword"
COLLECTION_NAME = "traffic_data"  # Target collection name

# --- Connect to ArangoDB _system database ---
client = ArangoClient(hosts=ARANGO_URL)
db = client.db(DB_NAME, username=USERNAME, password=PASSWORD)

# Create (or retrieve) the "traffic_data" collection.
if not db.has_collection(COLLECTION_NAME):
    traffic_data_collection = db.create_collection(COLLECTION_NAME)
    print(f"Created collection '{COLLECTION_NAME}' in '{DB_NAME}' database.")
else:
    traffic_data_collection = db.collection(COLLECTION_NAME)
    print(f"Using existing collection '{COLLECTION_NAME}' in '{DB_NAME}' database.")

def update_arango_from_excel(excel_filename, collection):
    try:
        df = pd.read_excel(excel_filename, engine="openpyxl")
    except Exception as e:
        print("Error reading Excel file:", e)
        return

    # Convert the 'timestamp' column to datetime for correct sorting.
    try:
        df['timestamp_dt'] = pd.to_datetime(df['timestamp'], format='%m/%d/%Y %H:%M:%S')
    except Exception as e:
        print("Error converting timestamp column:", e)
        return

    # For each cell_id, select the record with the latest timestamp.
    latest_df = df.sort_values('timestamp_dt').groupby('cell_id', as_index=False).last()

    # Upsert each document: update if exists; insert if new.
    for _, row in latest_df.iterrows():
        cell_key = str(int(row['cell_id']))  # Use cell_id as document key.
        doc = row.to_dict()
        doc.pop('timestamp_dt', None)

        if collection.has(cell_key):
            try:
                collection.update({'_key': cell_key, **doc})
                print(f"Updated document for cell_id {cell_key}")
            except Exception as e:
                print(f"Error updating cell {cell_key}: {e}")
        else:
            doc['_key'] = cell_key
            try:
                collection.insert(doc)
                print(f"Inserted document for cell_id {cell_key}")
            except Exception as e:
                print(f"Error inserting cell {cell_key}: {e}")

print(f"Starting updater using collection '{COLLECTION_NAME}' in database '{DB_NAME}'. Press Ctrl+C to stop.")

while True:
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Reading Excel and updating ArangoDB...")
    update_arango_from_excel(EXCEL_FILENAME, traffic_data_collection)
    time.sleep(UPDATE_INTERVAL)
