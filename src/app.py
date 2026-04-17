import streamlit as st
import pandas as pd
import os
import sys
import subprocess
import matplotlib.pyplot as plt
from PIL import Image
from streamlit_option_menu import option_menu

from utils.translator import translate_text
from ai_recommendations import (
    recommend_irrigation,
    recommend_fertilizer,
    recommend_crop
)
from predict_disease import predict_disease
import streamlit.components.v1 as components


# ------------------ TEXT TO SPEECH ------------------
def speak_text(text, lang_code):
    components.html(f"""
        <script>
            var msg = new SpeechSynthesisUtterance(`{text}`);
            msg.lang = "{lang_code}";
            msg.rate = 0.9;
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

# ------------------ PROJECT PATHS ------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# ------------------ SIDEBAR IMAGE ------------------
banner_path = os.path.join(BASE_DIR, "assets", "banner.png")

if os.path.exists(banner_path):
    st.sidebar.image(banner_path, use_container_width=True)

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

st.write(
    translate_text(
        "Interactively explore soil health, crop recommendations, and plant disease detection.",
        lang
    )
)

# ------------------ HORIZONTAL NAVIGATION ------------------
selected = option_menu(
    menu_title=None,
    options=["Dashboard", "Crop Disease Detection", "Researcher Lab"],
    icons=["bar-chart", "leaf", "flask"],
    orientation="horizontal"
)

st.divider()

# =========================================================
# DASHBOARD PAGE
# =========================================================
if selected == "Dashboard":

    # ------------------ DATA CONTROLS ------------------
    st.sidebar.subheader(translate_text("⚙️ Data Controls", lang))

    if st.sidebar.button(translate_text("🔄 Generate New Sensor Data", lang)):
        simulate_script = os.path.join(BASE_DIR, "src", "simulate_sensors.py")
        predict_script = os.path.join(BASE_DIR, "src", "predict_crops.py")

        subprocess.run([sys.executable, simulate_script], check=True)
        subprocess.run([sys.executable, predict_script], check=True)

        st.sidebar.success(
            translate_text("New data generated successfully!", lang)
        )

    # ------------------ LOAD DATA ------------------
    data_path = os.path.join(DATA_DIR, "predicted_crops.csv")

    if not os.path.exists(data_path):
        st.warning(
            translate_text(
                "No prediction data found. Please generate data using the button.",
                lang
            )
        )
        st.stop()

    df = pd.read_csv(data_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # ------------------ FILTERS ------------------
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
        translate_text(
            f"Showing {len(filtered)} records after filtering",
            lang
        )
    )

    # ------------------ TABLE ------------------
    st.subheader(
        translate_text("📋 Filtered Crop Predictions", lang)
    )

    st.dataframe(filtered, use_container_width=True)

    # ------------------ DISTRIBUTION ------------------
    st.subheader(
        translate_text("🌾 Crop Recommendation Distribution", lang)
    )

    st.bar_chart(filtered["recommended_crop"].value_counts())

    # ------------------ TIMELINE ------------------
    st.subheader(
        translate_text("📈 Predictions Over Time", lang)
    )

    timeline = filtered.groupby(
        filtered["timestamp"].dt.date
    )["recommended_crop"].count()

    fig, ax = plt.subplots(figsize=(10, 4))

    timeline.plot(ax=ax, marker="o")

    ax.set_xlabel(translate_text("Date", lang))
    ax.set_ylabel(translate_text("Prediction Count", lang))

    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    # ------------------ AI RECOMMENDATIONS ------------------
    st.subheader(
        translate_text("🤖 AI Recommendations (Latest Reading)", lang)
    )

    if not filtered.empty:

        latest = filtered.iloc[-1]

        irrigation_msg = recommend_irrigation(
            latest["soil_moisture"],
            latest["temperature"]
        )

        fertilizer_msg = recommend_fertilizer(
            latest["ph"],
            latest["N"],
            latest["P"],
            latest["K"]
        )

        crop_msg = recommend_crop(
            latest["temperature"],
            latest["humidity"],
            latest["rainfall"]
        )

        st.success(translate_text(irrigation_msg, lang))
        st.info(translate_text(fertilizer_msg, lang))
        st.warning(translate_text(crop_msg, lang))


# =========================================================
# CROP DISEASE DETECTION PAGE
# =========================================================
elif selected == "Crop Disease Detection":

    import numpy as np

    # -------- LEAF VALIDATION FUNCTION --------
    def is_leaf_image(image):
        img = np.array(image)

        # Ensure RGB
        if len(img.shape) < 3:
            return False

        red = img[:, :, 0]
        green = img[:, :, 1]
        blue = img[:, :, 2]

        # Check if green dominates (basic leaf detection)
        leaf_pixels = (green > red) & (green > blue)

        ratio = np.sum(leaf_pixels) / leaf_pixels.size

        return ratio > 0.20   # you can tune (0.15–0.30)

    # -------- UI --------
    st.header(translate_text("🌿 Crop Disease Detection", lang))

    st.subheader(
        translate_text(
            "📸 Capture or Upload Crop Leaf Image",
            lang
        )
    )

    # -------- CAMERA --------
    camera_enabled = st.toggle(
        translate_text("📷 Enable Camera", lang),
        value=False
    )

    camera_image = None

    if camera_enabled:
        camera_image = st.camera_input(
            translate_text("Scan Crop Leaf Using Camera", lang)
        )

    # -------- UPLOAD --------
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

    # -------- PROCESS --------
    if image_file is not None:

        image = Image.open(image_file).convert("RGB")

        st.image(
            image,
            caption=translate_text("Selected Leaf Image", lang),
            width=300
        )

        # =====================================================
        # STEP 1: LEAF CHECK
        # =====================================================
        if not is_leaf_image(image):
            st.error(
                translate_text(
                    "❌ Please upload a valid crop leaf image",
                    lang
                )
            )
            st.warning(
                translate_text(
                    "⚠️ The uploaded image does not appear to be a leaf.",
                    lang
                )
            )
            st.stop()

        # =====================================================
        # STEP 2: PREDICTION
        # =====================================================
        with st.spinner(
            translate_text("🔍 Analyzing leaf disease...", lang)
        ):
            label, confidence, info = predict_disease(image)

        # =====================================================
        # STEP 3: CONFIDENCE CHECK
        # =====================================================
        if confidence < 0.30:
            st.error(
                translate_text(
                    "❌ Unable to confidently detect disease. Try another clear leaf image.",
                    lang
                )
            )
            st.stop()

        # =====================================================
        # STEP 4: RESULT DISPLAY
        # =====================================================
        disease_name = label.split("_", 1)[-1].replace("_", " ")

        st.subheader(
            translate_text("🦠 Detected Disease", lang)
        )

        if "healthy" in label.lower():
            st.success(translate_text(f"✅ {disease_name}", lang))
        else:
            st.error(translate_text(f"🦠 {disease_name}", lang))

        # =====================================================
        # STEP 5: DETAILS
        # =====================================================
        st.subheader(
            translate_text("📖 Disease Details", lang)
        )

        st.write(translate_text(info["description"], lang))

        st.write("**" + translate_text("Precautions", lang) + ":**")
        st.write(translate_text(info["precautions"], lang))

        st.write("**" + translate_text("Treatment", lang) + ":**")
        st.write(translate_text(info["treatment"], lang))

        # =====================================================
        # STEP 6: VOICE OUTPUT
        # =====================================================
        full_voice_message = f"""
        {disease_name}.
        {info["description"]}.
        Precautions: {info["precautions"]}.
        Treatment: {info["treatment"]}.
        """

        if st.button("🔊 Speak Full Details"):
            speak_text(
                translate_text(full_voice_message, lang),
                lang
            )

# =========================================================
# RESEARCHER LAB PAGE
# =========================================================
elif selected == "Researcher Lab":

    import joblib

    st.header(translate_text("🔬 Researcher Lab", lang))

    st.write(
        translate_text(
            "Manually enter soil and weather values to test crop recommendation.",
            lang
        )
    )

    # ------------------ LOAD MODEL ------------------
    model_path = os.path.join(BASE_DIR, "models", "crop_recommendation_model.pkl")

    if not os.path.exists(model_path):
        st.error("Model file not found!")
        st.stop()

    model = joblib.load(model_path)

    # ------------------ INPUT FIELDS ------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        N = st.number_input("Nitrogen (N)", 0, 200, 50)
        P = st.number_input("Phosphorus (P)", 0, 200, 50)

    with col2:
        K = st.number_input("Potassium (K)", 0, 200, 50)
        ph = st.number_input("pH", 0.0, 14.0, 6.5)

    with col3:
        temperature = st.number_input("Temperature", 0.0, 50.0, 25.0)
        humidity = st.number_input("Humidity", 0.0, 100.0, 60.0)
        rainfall = st.number_input("Rainfall", 0.0, 500.0, 100.0)

    # ------------------ PREDICTION ------------------
    if st.button("Predict Crop Recommendation"):

        try:
            input_data = [[N, P, K, temperature, humidity, ph, rainfall]]

            prediction = model.predict(input_data)
            result = prediction[0]

            st.success(f"🌾 Recommended Crop: {result}")

        except Exception as e:
            st.error(f"Error: {e}")