import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# File paths
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "Crop_recommendation.csv")
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "crop_recommendation_model.pkl")

print("📂 Loading dataset...")
df = pd.read_csv(DATA_PATH)

# Display first few rows
print("\n🧾 Sample Data:")
print(df.head())

# Features (inputs) and Target (output)
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train RandomForest model
print("\n🌱 Training Random Forest model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Model Accuracy: {accuracy * 100:.2f}%")

# Save trained model
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump(model, MODEL_PATH)
print(f"💾 Model saved to: {MODEL_PATH}")

# Optional detailed report
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))