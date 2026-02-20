import pandas as pd
import random
from datetime import datetime, timedelta
import os

print("🌾 Generating realistic sensor data (aligned with Kaggle ranges)...")

# Define realistic Kaggle-based value ranges
def random_value(min_v, max_v):
    return round(random.uniform(min_v, max_v), 2)

farms = [1, 2, 3, 4, 5]
rows = []

for _ in range(100):
    timestamp = (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
    farm_id = random.choice(farms)
    row = {
        'timestamp': timestamp,
        'farm_id': farm_id,
        'N': random_value(0, 140),
        'P': random_value(5, 120),
        'K': random_value(5, 200),
        'pH': random_value(4, 9),
        'temperature_C': random_value(15, 45),
        'humidity_percent': random_value(30, 95),
        'soil_moisture_percent': random_value(10, 90),
        'rainfall_mm': random_value(20, 300)
    }
    rows.append(row)

df = pd.DataFrame(rows)

# 🔹 Get project root (parent of src)
SRC_FOLDER = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(SRC_FOLDER)

# 🔹 Path to existing data folder outside src
data_path = os.path.join(PROJECT_ROOT, "data", "cleaned_sensor_data.csv")

df.to_csv(data_path, index=False)

print(f"✅ Saved realistic sensor data to: {data_path}")
print(df.head())
