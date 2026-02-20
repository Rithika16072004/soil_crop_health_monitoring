import streamlit as st
import pandas as pd
import os
import sys
import subprocess
import matplotlib.pyplot as plt
from PIL import Image

from utils.translator import translate_text
from ai_recommendations import (
    recommend_irrigation,
    recommend_fertilizer,
    recommend_crop
)
from predict_disease import predict_disease
import streamlit.components.v1 as components

def speak_text(text, lang_code):
    components.html(f"""
        <script>
            var msg = new SpeechSynthesisUtterance(`{text}`);
            msg.lang = "{lang_code}";
            msg.rate = 0.9;      // slightly slower
            msg.pitch = 1;
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(msg);
        </script>
    """, height=0)



# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="🌾 Smart Agriculture Dashboard",
    layout="wide"
)

# ------------------ LANGUAGE SELECTOR ------------------
language = st.sidebar.selectbox(
    "🌐 Select Language",
    ["English", "தமிழ்", "हिन्दी"]
)

LANG_MAP = {
    "English": "en",
    "தமிழ்": "ta",
    "हिन्दी": "hi"
}
lang = LANG_MAP[language]

# ------------------ TITLE ------------------
st.title(translate_text("🌱 AI-Powered Crop & Plant Health Monitoring System", lang))
st.write(translate_text(
    "Interactively explore soil health, crop recommendations, and plant disease detection.",
    lang
))

# ------------------ PROJECT PATHS ------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# ------------------ DATA GENERATION BUTTON ------------------
st.sidebar.subheader(translate_text("⚙️ Data Controls", lang))

if st.sidebar.button(translate_text("🔄 Generate New Sensor Data", lang)):
    simulate_script = os.path.join(BASE_DIR, "src", "simulate_sensors.py")
    predict_script = os.path.join(BASE_DIR, "src", "predict_crops.py")

    subprocess.run([sys.executable, simulate_script], check=True)
    subprocess.run([sys.executable, predict_script], check=True)

    st.sidebar.success(translate_text("New data generated successfully!", lang))

# ------------------ LOAD DATA ------------------
data_path = os.path.join(DATA_DIR, "predicted_crops.csv")

if not os.path.exists(data_path):
    st.warning(translate_text(
        "No prediction data found. Please generate data using the button.",
        lang
    ))
    st.stop()

df = pd.read_csv(data_path)
df["timestamp"] = pd.to_datetime(df["timestamp"])

# ------------------ SIDEBAR FILTERS ------------------
st.sidebar.header(translate_text("🔍 Filter Options", lang))

farms = sorted(df["farm_id"].unique())
selected_farms = st.sidebar.multiselect(
    translate_text("🏡 Select Farm(s)", lang),
    farms,
    default=farms
)

crops = sorted(df["recommended_crop"].unique())
selected_crops = st.sidebar.multiselect(
    translate_text("🌾 Select Crop(s)", lang),
    crops,
    default=crops
)


# ------------------ FILTER DATA ------------------
filtered = df[
    (df["farm_id"].isin(selected_farms)) &
    (df["recommended_crop"].isin(selected_crops))
]

st.success(
    translate_text(f"Showing {len(filtered)} records after filtering", lang)
)

# ------------------ TABLE ------------------
st.subheader(translate_text("📋 Filtered Crop Predictions", lang))
st.dataframe(filtered, use_container_width=True)

# ------------------ DISTRIBUTION ------------------
st.subheader(translate_text("🌾 Crop Recommendation Distribution", lang))
st.bar_chart(filtered["recommended_crop"].value_counts())

# ------------------ TIMELINE ------------------
st.subheader(translate_text("📈 Predictions Over Time", lang))

timeline = filtered.groupby(filtered["timestamp"].dt.date)["recommended_crop"].count()

fig, ax = plt.subplots(figsize=(10, 4))  # 👈 wider figure
timeline.plot(ax=ax, marker="o")

ax.set_xlabel(translate_text("Date", lang))
ax.set_ylabel(translate_text("Prediction Count", lang))

ax.tick_params(axis="x", rotation=45)    # 👈 rotate dates
fig.tight_layout()                        # 👈 auto spacing fix

st.pyplot(fig)
plt.close(fig)


# ------------------ AI RECOMMENDATIONS ------------------
st.subheader(translate_text("🤖 AI Recommendations (Latest Reading)", lang))

if not filtered.empty:
    latest = filtered.iloc[-1]

    irrigation_msg = recommend_irrigation(
        latest["soil_moisture"], latest["temperature"]
    )
    fertilizer_msg = recommend_fertilizer(
        latest["ph"], latest["N"], latest["P"], latest["K"]
    )
    crop_msg = recommend_crop(
        latest["temperature"], latest["humidity"], latest["rainfall"]
    )

    st.success(translate_text(irrigation_msg, lang))
    st.info(translate_text(fertilizer_msg, lang))
    st.warning(translate_text(crop_msg, lang))

# ======================================================
# 🌿 PLANT DISEASE DETECTION
# ======================================================
# ======================================================
# 🌿 PLANT DISEASE DETECTION
# ======================================================
st.divider()
st.header(translate_text("🌿 Crop Disease Detection", lang))

st.subheader(translate_text("📸 Capture or Upload Crop Leaf Image", lang))

# -------- CAMERA TOGGLE (Prevents Auto Opening) --------
camera_enabled = st.toggle(
    translate_text("📷 Enable Camera", lang),
    value=False
)

camera_image = None

if camera_enabled:
    camera_image = st.camera_input(
        translate_text("Scan Crop Leaf Using Camera", lang),
        key="leaf_camera"
    )

# -------- FILE UPLOADER --------
uploaded_file = st.file_uploader(
    translate_text("Or Upload Crop Leaf Image", lang),
    type=["jpg", "png", "jpeg"]
)

# -------- SELECT IMAGE --------
image_file = None

if camera_image is not None:
    image_file = camera_image
elif uploaded_file is not None:
    image_file = uploaded_file

# -------- DISEASE PREDICTION --------
if image_file is not None:

    image = Image.open(image_file)

    st.image(
        image,
        caption=translate_text("Selected Leaf Image", lang),
        width=300
    )

    with st.spinner(translate_text("🔍 Analyzing leaf disease...", lang)):
        label, confidence, info = predict_disease(image)

    disease_name = label.split("_", 1)[-1].replace("_", " ")

    st.subheader(translate_text("🦠 Detected Disease", lang))

    if "healthy" in label.lower():
        st.success(translate_text(f"✅ {disease_name}", lang))
    else:
        st.error(translate_text(f"🦠 {disease_name}", lang))
        # -------- DETAILS --------
    st.subheader(translate_text("📖 Disease Details", lang))

    st.write(translate_text(info["description"], lang))

    st.write("**" + translate_text("Precautions", lang) + ":**")
    st.write(translate_text(info["precautions"], lang))

    st.write("**" + translate_text("Treatment", lang) + ":**")
    st.write(translate_text(info["treatment"], lang))

    # -------- VOICE OUTPUT (Full Explanation) --------

    full_voice_message = f"""
    {disease_name}.
    {info["description"]}.
    Precautions: {info["precautions"]}.
    Treatment: {info["treatment"]}.
    """

    if st.button("🔊 Speak Full Details"):
        speak_text(translate_text(full_voice_message, lang), lang)
