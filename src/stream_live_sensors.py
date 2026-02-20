import pandas as pd
import random
import time
from datetime import datetime
import joblib
import os

print("🚜 Starting live sensor simulation... (Press Ctrl+C to stop)")

# -------- PROJECT ROOT --------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "diverse_crop_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "predicted_crops.csv")

# Load trained model
model = joblib.load(MODEL_PATH)

while True:
    row = {
        'timestamp': datetime.now().isoformat(),
        'farm_id': random.choice([1, 2, 3, 4, 5]),
        'N': round(random.uniform(0, 140), 2),
        'P': round(random.uniform(5, 120), 2),
        'K': round(random.uniform(5, 200), 2),
        'pH': round(random.uniform(4, 9), 2),
        'temperature_C': round(random.uniform(15, 45), 2),
        'humidity_percent': round(random.uniform(30, 95), 2),
        'soil_moisture_percent': round(random.uniform(10, 90), 2),
        'rainfall_mm': round(random.uniform(20, 300), 2)
    }

    df = pd.DataFrame([row])

    df = df.rename(columns={
        'temperature_C': 'temperature',
        'humidity_percent': 'humidity',
        'rainfall_mm': 'rainfall',
        'pH': 'ph'
    })

    features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    df['recommended_crop'] = model.predict(df[features])

    df[['timestamp', 'farm_id', 'recommended_crop']].to_csv(
        DATA_PATH,
        mode='a',
        header=not os.path.exists(DATA_PATH),
        index=False
    )

    print(f"🌱 New data added — Farm {row['farm_id']}: {df['recommended_crop'].iloc[0]}")
    time.sleep(10)
