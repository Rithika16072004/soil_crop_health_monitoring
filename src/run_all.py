import os
import subprocess
import time
import random
import firebase_admin
from firebase_admin import credentials, firestore

# ---------------- Firebase ----------------
def init_firebase():
    if not firebase_admin._apps:
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        firebase_key_path = os.path.join(BASE_DIR, "cloud", "firebase-key.json")
        cred = credentials.Certificate(firebase_key_path)
        firebase_admin.initialize_app(cred)
    return firestore.client()

def clear_old_data(db):
    docs = db.collection("sensor_data").stream()
    batch = db.batch()
    count = 0
    for doc in docs:
        batch.delete(doc.reference)
        count += 1
    batch.commit()
    print(f"🧹 Cleared {count} old sensor records.\n")

def upload_random_sensor_data():
    db = init_firebase()
    clear_old_data(db)
    farms = [1, 2, 3, 4, 5]
    print("🚀 Uploading fresh sensor data to Firestore...\n")
    for i in range(10):
        farm_id = random.choice(farms)
        temperature_c = round(random.uniform(20, 42), 2)
        humidity_percent = round(random.uniform(40, 95), 2)
        soil_moisture_percent = round(random.uniform(10, 90), 2)
        n = round(random.uniform(20, 200), 2)
        p = round(random.uniform(10, 150), 2)
        k = round(random.uniform(10, 180), 2)
        ph = round(random.uniform(4.5, 8.5), 2)
        rainfall_mm = round(random.uniform(40, 300), 2)

        if soil_moisture_percent < 30:
            message = "Low soil moisture — irrigation needed"
        elif ph < 5.5:
            message = "Soil too acidic — add lime"
        elif temperature_c > 38:
            message = "High temperature — crop stress risk"
        else:
            message = "All conditions normal"

        data = {
            "farm_id": farm_id,
            "temperature_c": temperature_c,
            "humidity_percent": humidity_percent,
            "soil_moisture_percent": soil_moisture_percent,
            "n": n,
            "p": p,
            "k": k,
            "ph": ph,
            "rainfall_mm": rainfall_mm,
            "message": message,
            "timestamp": firestore.SERVER_TIMESTAMP,
        }

        doc_id = f"farm_{farm_id}_{i}"
        db.collection("sensor_data").document(doc_id).set(data)
        print(f"✅ Uploaded Farm {farm_id}: {message}")
        time.sleep(0.2)

    print("\n🌿 Upload complete! Waiting for Firestore to finalize timestamps...")
    time.sleep(5)
    print("✅ Ready to view in dashboard.\n")

# ---------------- Predict crops ----------------
def predict_crops():
    """Call predict_crops.py to generate predicted_crops.csv"""
    SRC_FOLDER = os.path.dirname(__file__)
    predict_script = os.path.join(SRC_FOLDER, "predict_crops.py")
    print("🤖 Running crop prediction script...")
    subprocess.run(["python", predict_script], check=True)
    print("✅ Crop predictions generated.\n")

# ---------------- Launch dashboard ----------------
def launch_dashboard():
    SRC_FOLDER = os.path.dirname(__file__)
    dashboard_path = os.path.join(SRC_FOLDER, "cloud_dashboard.py")
    dashboard_path = os.path.abspath(dashboard_path)
    print("📊 Launching Streamlit dashboard...")
    subprocess.run(["streamlit", "run", dashboard_path], shell=True)

# ---------------- Main ----------------
if __name__ == "__main__":
    upload_random_sensor_data()
    predict_crops()  # ✅ Generate predicted_crops.csv before dashboard
    launch_dashboard()
