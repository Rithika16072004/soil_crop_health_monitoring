# 🌾 AI-Powered Smart Agriculture & Plant Health Monitoring System

An intelligent agriculture dashboard that combines crop recommendation, sensor-based analytics, and plant disease detection using AI.

This project is designed to assist farmers with smart decision-making through multilingual support and voice-enabled outputs.

---

## 🚀 Features

### 🌱 1. Crop Recommendation System
- Recommends best crops based on:
  - Temperature
  - Humidity
  - Rainfall
  - Soil nutrients (N, P, K)
- Uses Machine Learning models

### 📊 2. Smart Agriculture Dashboard
- Interactive data visualization
- Crop distribution charts
- Timeline predictions
- Farm filtering options
- Sensor data simulation

### 🌿 3. Plant Disease Detection
- Upload or capture crop leaf image
- Deep Learning CNN model
- Detects disease & confidence level
- Displays:
  - Disease Description
  - Precautions
  - Treatment Suggestions

### 🌐 4. Multilingual Support
Supports:
- English 🇬🇧
- Tamil 🇮🇳
- Hindi 🇮🇳

Uses `deep-translator` for dynamic translation.

### 🔊 5. Voice Output (Farmer Friendly)
- Reads disease description
- Reads precautions
- Reads treatment
- Works in selected language
- Browser-based Speech Synthesis

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Matplotlib
- Scikit-Learn
- TensorFlow / Keras (for disease detection)
- Deep Translator
- HTML + JavaScript (for voice output)

---

## 📁 Project Structure

```
Final_year_project/
│
├── src/
│   ├── app.py
│   ├── ai_recommendations.py
│   ├── predict_disease.py
│   └── ...
│
├── models/
│   ├── plant_disease_model.h5
│   ├── crop_recommendation_model.pkl
│
├── data/
├── utils/
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation (Local Setup)

1. Clone repository:

```
git clone https://github.com/YOUR_USERNAME/final-year-project.git
cd final-year-project
```

2. Create virtual environment:

```
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Run the application:

```
streamlit run src/app.py
```

---

## 🌍 Deployment

This project can be deployed using:

- Streamlit Cloud

Public deployment allows:
- 24/7 access
- Mobile compatibility
- Camera access
- Voice support

---

## 🎯 Project Objective

To build a farmer-friendly AI system that:
- Improves crop productivity
- Detects plant diseases early
- Provides treatment guidance
- Supports regional languages
- Uses voice for accessibility

---

## 📌 Future Enhancements

- Mobile app integration
- IoT sensor integration
- SMS alerts for farmers
- Cloud database integration
- Real-time weather API support

---

## 👩‍💻 Developed By

Final Year Engineering Project  
Department of Computer Science / Artificial Intelligence  

---

## 📄 License

This project is developed for academic purposes.
