import firebase_admin
from firebase_admin import credentials, firestore
import time

# ✅ Firebase key
cred = credentials.Certificate(r"C:\Users\Rithi\OneDrive\Documents\Final_year_project\cloud\firebase-key.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

print("🌤️ Cloud Alert System Started — monitoring Firestore for sensor warnings...")

def check_alerts(doc):
    data = doc.to_dict()
    alerts = []

    if data.get("soil_moisture_percent", 0) < 25:
        alerts.append("🚨 Low soil moisture! Immediate irrigation needed.")
    if data.get("temperature_C", 0) > 38:
        alerts.append("🔥 High temperature detected! Consider shade or early watering.")
    if data.get("pH", 7) < 5.5:
        alerts.append("🧪 Soil too acidic! Apply lime to balance pH.")
    if data.get("pH", 7) > 8.5:
        alerts.append("🧪 Soil too alkaline! Consider organic compost.")

    if alerts:
        print("\n⚠️ ALERT for farm_id:", data.get("farm_id", "Unknown"))
        for a in alerts:
            print("   -", a)
        print("-------------------------")

# 🔄 Continuous monitoring
while True:
    docs = db.collection("sensor_data").stream()
    for doc in docs:
        check_alerts(doc)
    time.sleep(10)  # Check every 10 seconds