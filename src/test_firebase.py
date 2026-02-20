import firebase_admin
from firebase_admin import credentials, firestore

print("🌾 Connecting to Firebase...")

# ✅ Use the full absolute path to your Firebase key file
cred = credentials.Certificate("C:/Users/rosha/Documents/CropSoilAI/cloud/firebase-key.json")

# Initialize Firebase app
firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

# Test: add a simple document
data = {
    "N": 45,
    "P": 55,
    "K": 65,
    "pH": 6.8,
    "temperature": 28,
    "humidity": 70,
    "message": "🌾 Firebase connection successful!"
}

# Add document to a collection called 'sensor_data'
db.collection("sensor_data").add(data)

print("✅ Data successfully added to Firestore!")