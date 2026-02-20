import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import time

print("🌾 Uploading real sensor data to Firestore...")

# ✅ Firebase key absolute path
cred = credentials.Certificate(r"C:\Users\Rithi\OneDrive\Documents\Final_year_project\cloud\firebase-key.json")

# Initialize Firebase app (only if not already initialized)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ✅ Load your cleaned sensor data
csv_path = r"C:\Users\Rithi\OneDrive\Documents\Final_year_project\data\cleaned_sensor_data.csv"
df = pd.read_csv(csv_path)

print(f"✅ Loaded {len(df)} sensor records from {csv_path}")

# Upload each record to Firestore
for i, row in df.iterrows():
    data = {
        "timestamp": row["timestamp"],
        "farm_id": int(row["farm_id"]),
        "N": float(row["N"]),
        "P": float(row["P"]),
        "K": float(row["K"]),
        "pH": float(row["pH"]),
        "temperature_C": float(row["temperature_C"]),
        "humidity_percent": float(row["humidity_percent"]),
        "soil_moisture_percent": float(row["soil_moisture_percent"]),
        "rainfall_mm": float(row["rainfall_mm"]),
    }
    db.collection("sensor_data").add(data)
    print(f"📤 Uploaded record {i+1}/{len(df)}")
    time.sleep(0.1)  # small delay to avoid rate limits

print("✅ All sensor data uploaded successfully to Firestore!")