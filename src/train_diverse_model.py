import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import os

print("🌾 Training AI Model on Diverse Crop Dataset...")

# Load dataset
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # Final_year_project

DATA_PATH = os.path.join(BASE_DIR, "data", "Crop_recommendation.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "diverse_crop_model.pkl")
os.makedirs(MODEL_DIR, exist_ok=True)
# ---------------------------------

# Load dataset
df = pd.read_csv(DATA_PATH)

print("✅ Dataset loaded successfully!")
print("Columns:", list(df.columns))
print("Sample data:")
print(df.head())

# Split features and target
X = df.drop("label", axis=1)
y = df["label"]

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\n🎯 Model Accuracy: {acc:.2f}")
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, MODEL_PATH)
print(f"\n✅ Model saved at: {MODEL_PATH}")
