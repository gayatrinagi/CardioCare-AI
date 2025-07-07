import streamlit as st

st.set_page_config(page_title="About", layout="centered")

st.title("📖 About This App")

st.markdown("""
This application predicts the likelihood of heart complications in individuals who have recovered from COVID-19, using a machine learning model trained on health and post-COVID data.

---
### 💓 Why Post-COVID Heart Risk Matters
COVID-19 can impact the cardiovascular system even after recovery, potentially leading to:
- 🫀 Myocarditis (heart inflammation)
- ⚡ Arrhythmia (irregular heartbeat)
- 🧠 Stroke or clotting disorders

Certain populations (e.g., those with diabetes or hypertension) are more vulnerable.

---
### 💉 Vaccine Impact Summary
Our model integrates vaccine type (Covaxin, Covishield, Pfizer, or None) as a feature to study its influence on predicted risk.

📊 **Initial observations** (from sample data):
- Vaccinated individuals generally showed **lower predicted heart risk**
- Pfizer and Covaxin users had slightly lower model risk predictions than those unvaccinated or with Covishield
- **NOTE**: These are simulated insights for educational purposes, not clinical claims.

---
### 🧠 Post-COVID Health Tips
Following COVID-19 recovery, especially if you had a severe case:

- 🏃‍♂️ Resume physical activity **gradually**
- 💧 Stay hydrated and monitor vital signs (BP, heart rate)
- 🍎 Maintain a balanced diet with anti-inflammatory foods
- 💤 Prioritize sleep and mental health recovery
- 📆 Visit your doctor for regular follow-ups if you're high risk

---
### ⚠️ When to Seek Medical Help
You should **consult a doctor immediately** if you experience:
- Chest discomfort or tightness
- Shortness of breath while resting
- Irregular heartbeat
- Swelling in legs or feet

---
### 🛠 App & Model Details
- **Model Used**: Random Forest Classifier
- **Input Features**: Age, BP, Cholesterol, Vaccine Type, Hospitalization, etc.
- **Explainability**: SHAP summary plots
- **Prediction Output**: High Risk / Low Risk

---
### 🌐 Intended Use
This is a **health awareness tool**, not a diagnostic system. It's built for:
- Public awareness campaigns
- Educational and analytical use
- Screening before professional consultation

---
### 🚀 Future Enhancements
- PDF report generation
- Per-user health tracking dashboards
- Backend API for mobile integration
- Integration with real-world health data (EHRs, FHIR)

---
### 🙌 Built by
Nagig • Streamlit | Scikit-learn | SHAP

Stay healthy. Stay informed.
""")
