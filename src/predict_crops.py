import pandas as pd
import joblib
import os

print("📦 Loading trained crop recommendation model...")

# -------- PROJECT ROOT PATH SETUP --------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")

# ----------------------------------------

# Load trained model
model_path = os.path.join(MODEL_DIR, "diverse_crop_model.pkl")
model = joblib.load(model_path)
print(f"✅ Loaded model from: {model_path}")

print("📂 Loading cleaned sensor data...")

# Load cleaned dataset
data_path = os.path.join(DATA_DIR, "simulated_sensor_data.csv")

df = pd.read_csv(data_path)

print("\n🧾 Columns found in cleaned dataset:")
print(list(df.columns))

# Rename columns to match training data
rename_map = {
    'temperature_C': 'temperature',
    'humidity_percent': 'humidity',
    'rainfall_mm': 'rainfall',
    'soil_moisture_percent': 'soil_moisture',
    'pH': 'ph'
}


df = df.rename(columns=rename_map)

# Required columns (same order as training)
required_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
    raise KeyError(f"❌ Missing columns in data: {missing_cols}")

input_data = df[required_columns]

print("\n🤖 Making crop predictions...")
predictions = model.predict(input_data)

# Add predictions
df['recommended_crop'] = predictions

# Save output
output_path = os.path.join(DATA_DIR, "predicted_crops.csv")
columns_to_save = [
    'timestamp',
    'farm_id',
    'soil_moisture',
    'temperature',
    'humidity',
    'rainfall',
    'ph',
    'N',
    'P',
    'K',
    'recommended_crop'
]

df[columns_to_save].to_csv(output_path, index=False)


print(f"\n✅ Predictions saved to: {output_path}")

print("\n🌾 Sample predictions:")
print(df[['timestamp', 'farm_id', 'recommended_crop']].head())
