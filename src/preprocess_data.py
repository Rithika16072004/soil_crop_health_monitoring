import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import os

# Path to the original CSV file
INPUT_CSV = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "simulated_sensor_data.csv")
OUTPUT_CSV = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cleaned_sensor_data.csv")

print("📂 Loading dataset...")
df = pd.read_csv(INPUT_CSV)

# 1️⃣ Show first 5 rows
print("\n🧾 First 5 rows of the dataset:")
print(df.head())

# 2️⃣ Check general info
print("\n📊 Dataset Info:")
print(df.info())

# 3️⃣ Basic statistics
print("\n📈 Statistical Summary:")
print(df.describe())

# 4️⃣ Check for missing values
print("\n🔍 Checking for missing values:")
print(df.isnull().sum())

# If missing values exist, fill them with column mean
df = df.fillna(df.mean(numeric_only=True))

# 5️⃣ Normalize numeric columns (except timestamp and farm_id)
numeric_cols = ['N', 'P', 'K', 'pH', 'temperature_C', 'humidity_percent', 'soil_moisture_percent', 'rainfall_mm']
scaler = StandardScaler()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# 6️⃣ Save cleaned dataset
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
df.to_csv(OUTPUT_CSV, index=False)
print(f"\n✅ Cleaned dataset saved to: {OUTPUT_CSV}")

# 7️⃣ Show confirmation
print("\n🧩 Columns in cleaned data:")
print(df.columns.tolist())

print("\n✅ Data preprocessing completed successfully.")