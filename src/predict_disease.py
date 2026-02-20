import tensorflow as tf
import numpy as np
import json
from PIL import Image
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "plant_disease_model.h5")
INFO_PATH = os.path.join(BASE_DIR, "disease_info", "disease_info.json")
CLASS_PATH = os.path.join(BASE_DIR, "models", "class_indices.json")

# ---------- LOAD MODEL ----------
model = tf.keras.models.load_model(MODEL_PATH)

# ---------- LOAD DISEASE INFO ----------
with open(INFO_PATH, "r") as f:
    disease_info = json.load(f)

# ---------- LOAD CLASS INDICES ----------
with open(CLASS_PATH, "r") as f:
    class_indices = json.load(f)

# Invert dict → index : class_name
IDX_TO_CLASS = {v: k for k, v in class_indices.items()}


# ---------- CLEAN LABEL ----------
def clean_disease_name(label: str):
    """
    Remove crop name and format disease nicely
    """
    label = label.replace("_", " ")

    # Remove crop names
    for crop in ["Tomato", "Potato", "Pepper__bell", "Pepper"]:
        label = label.replace(crop, "")

    label = label.strip()
    return label.title()


# ---------- PREDICTION ----------
def predict_disease(image: Image.Image):
    image = image.convert("RGB")
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)

    preds = model.predict(image, verbose=0)
    idx = int(np.argmax(preds))
    confidence = float(np.max(preds))

    original_label = IDX_TO_CLASS[idx]
    cleaned_label = clean_disease_name(original_label)

    info = disease_info.get(original_label, {
        "description": "No information available.",
        "precautions": "N/A",
        "treatment": "N/A"
    })

    return cleaned_label, confidence, info
