import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import time
import altair as alt
from ai_recommendations import recommend_irrigation, recommend_fertilizer, recommend_crop

# ============================================================
# 🔥 Firebase Safe Init
# ============================================================
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(r"C:\Users\Rithi\OneDrive\Documents\Final_year_project\cloud\firebase-key.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    st.error(f"⚠️ Firebase init failed: {e}")
    db = None

# ============================================================
# 🌐 Streamlit Config
# ============================================================
st.set_page_config(page_title="☁️ Cloud Crop & Soil Dashboard", layout="wide")
st.title("☁️ Cloud-Connected Crop & Soil Health Dashboard")

# ============================================================
# 📥 Load Firestore Data
# ============================================================
@st.cache_data(ttl=20)
def load_sensor_data():
    if db is None:
        raise ConnectionError("Firebase not initialized properly.")
    docs = db.collection("sensor_data").stream()
    data = [doc.to_dict() for doc in docs if doc.to_dict()]
    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.loc[:, ~df.columns.duplicated()]

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
        df["timestamp"] = df["timestamp"].dt.tz_convert(None)

    return df.sort_values("timestamp", ascending=False)

# ============================================================
# 🧭 Sidebar Controls
# ============================================================
st.sidebar.header("🌍 Dashboard Controls")

# Farm filter
selected_farm = "All Farms"
if db:
    try:
        farms = sorted(list(set([doc.to_dict().get("farm_name", "Unknown")
                                 for doc in db.collection("sensor_data").stream()])))
        if farms:
            selected_farm = st.sidebar.selectbox("🏡 Select Farm", ["All Farms"] + farms)
    except Exception:
        pass

# Manual refresh
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# Auto-refresh
st.sidebar.markdown("⏱️ Auto-refresh enabled (10 s)")
auto_refresh = st.sidebar.checkbox("Auto-refresh", value=True)
if auto_refresh:
    st.experimental_rerun_interval = 10

st.sidebar.markdown("---")
st.sidebar.info("Use filters to explore specific farms and metrics in real time.")

# ============================================================
# 📊 Main Dashboard
# ============================================================
with st.spinner("Fetching latest Firestore data..."):
    df = load_sensor_data()

if df.empty:
    st.warning("⚠️ No sensor data found in Firestore.")
    st.stop()

# Filter by farm
if selected_farm != "All Farms" and "farm_name" in df.columns:
    df = df[df["farm_name"] == selected_farm]

# ============================================================
# 📋 Live Firestore Table (Styled)
# ============================================================
st.subheader("📊 Live Sensor Data from Firestore")

df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce").astype(str)

def style_table(df):
    if "farm_id" in df.columns:
        colors = {1: "#E6F3FF", 2: "#FFF6E6", 3: "#E6FFE6", 4: "#FDE6FF"}
        styled = df.style.apply(
            lambda row: [
                f"background-color: {colors.get(row.farm_id, '#F9F9F9')}" for _ in row
            ],
            axis=1,
        )
    else:
        styled = df.style.set_properties(**{"background-color": "#FAFAFA"})
    return styled.format(precision=2)

compact = st.toggle("🔎 Compact View (hide less important columns)", value=False)

display_df = df.copy()
if compact:
    keep = ["farm_id", "timestamp", "temperature_c", "humidity_percent",
            "soil_moisture_percent", "ph", "message"]
    display_df = df[[c for c in keep if c in df.columns]]

st.dataframe(style_table(display_df), use_container_width=True, height=400)

csv = display_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Data as CSV",
    data=csv,
    file_name="sensor_data.csv",
    mime="text/csv",
    use_container_width=True,
)

# ============================================================
# 🌡️ Metrics Overview
# ============================================================
st.subheader("📈 Current Farm Statistics")
if all(x in df.columns for x in ["temperature_c", "humidity_percent", "soil_moisture_percent"]):
    c1, c2, c3 = st.columns(3)
    c1.metric("🌡️ Avg Temp", f"{df['temperature_c'].mean():.1f} °C")
    c2.metric("💧 Avg Humidity", f"{df['humidity_percent'].mean():.1f} %")
    c3.metric("🌱 Avg Moisture", f"{df['soil_moisture_percent'].mean():.1f} %")

# ============================================================
# 📉 Trend Charts
# ============================================================
st.subheader("📉 Sensor Data Trends")

if "timestamp" in df.columns:
    if "temperature_c" in df.columns:
        st.altair_chart(
            alt.Chart(df).mark_line(point=True).encode(
                x="timestamp:T", y="temperature_c:Q",
                color=alt.value("#E74C3C")
            ).properties(title="🌡️ Temperature Over Time"),
            use_container_width=True,
        )

    if "soil_moisture_percent" in df.columns:
        st.altair_chart(
            alt.Chart(df).mark_area(opacity=0.5).encode(
                x="timestamp:T", y="soil_moisture_percent:Q",
                color=alt.value("#27AE60")
            ).properties(title="💧 Soil Moisture Over Time"),
            use_container_width=True,
        )

# ============================================================
# 🚨 Alerts
# ============================================================
st.subheader("🚨 Real-Time Farm Alerts")
latest = df.iloc[0]

if latest["soil_moisture_percent"] < 30:
    st.error("💧 *Irrigation Needed* — Soil moisture critically low!")
elif latest["soil_moisture_percent"] > 80:
    st.warning("🌊 Soil too wet — drainage may be needed.")
else:
    st.success("✅ Soil moisture is optimal.")

if latest["temperature_c"] > 38:
    st.warning("🔥 Crop Stress Warning — High temperature detected!")
elif latest["temperature_c"] < 15:
    st.info("❄️ Low temperature — crop growth may slow.")
else:
    st.success("🌤️ Temperature within healthy range.")

if latest.get("ph", 7) < 5.5 or latest.get("ph", 7) > 7.5:
    st.error("🧪 Soil acidity imbalance — pH out of ideal range!")
else:
    st.success("🧪 Soil pH is balanced.")

# ============================================================
# 🤖 AI Recommendations
# ============================================================
st.subheader("🤖 Smart AI Recommendations")
irrigation = recommend_irrigation(latest["soil_moisture_percent"], latest["temperature_c"])
fertilizer = recommend_fertilizer(latest["ph"], latest["n"], latest["p"], latest["k"])
crop_suggestion = recommend_crop(latest["temperature_c"], latest["humidity_percent"], latest["rainfall_mm"])

st.markdown(f"*💧 Irrigation Advice:* {irrigation}")
st.markdown(f"*🌿 Fertilizer Advice:* {fertilizer}")
st.markdown(f"*🌾 Crop Suggestion:* {crop_suggestion}")

# ============================================================
# 🧠 AI Summary
# ============================================================
st.subheader("🧠 AI Summary Insight")
summary = f"""
- Current temperature: *{latest['temperature_c']} °C, humidity: *{latest['humidity_percent']} %**.  
- Soil moisture: *{latest['soil_moisture_percent']} %*, indicating {'dry conditions — irrigation needed' if latest['soil_moisture_percent'] < 30 else 'healthy soil'}.  
- Soil pH: *{latest.get('ph', 'N/A')}*, suggesting {'acidic' if latest.get('ph',7) < 6 else 'neutral/basic'} soil.  
- Recommended crop: *{crop_suggestion}*.
"""
st.info(summary)

# ============================================================
# 🕒 Footer
# ============================================================
st.markdown("---")
st.caption("🕒 Last updated: " + time.strftime("%Y-%m-%d %H:%M:%S"))