import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "datasets", "PlantVillage")
MODEL_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODEL_DIR, exist_ok=True)

IMG_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 6   # 🔥 ONLY 6 EPOCHS

datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=25,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train_data = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training"
)

val_data = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation"
)

# 🔥 PRETRAINED MODEL
base_model = MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False  # freeze base layers

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation="relu")(x)
output = Dense(train_data.num_classes, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=output)

model.compile(
    optimizer=Adam(learning_rate=0.0003),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS
)

# ✅ SAVE MODEL
model.save(os.path.join(MODEL_DIR, "plant_disease_model.h5"))

# ✅ SAVE CLASS INDICES (VERY IMPORTANT)
with open(os.path.join(MODEL_DIR, "class_indices.json"), "w") as f:
    json.dump(train_data.class_indices, f)

print("✅ Training completed using MobileNetV2")
