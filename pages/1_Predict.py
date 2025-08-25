# pages/1_Predict.py
import streamlit as st
import pandas as pd
import joblib
from utils.db_manager import save_history

st.title("🔍 Post-COVID Heart Risk & Insurance Estimator")

# Gate: must be logged in
if not st.session_state.get("logged_in", False):
    st.warning("🔒 Please log in on the **0_Login** page to access the prediction tool.")
    st.stop()

email = st.session_state.get("email", "guest@demo.com")

# Lazy-load model with helpful error
@st.cache_resource(show_spinner=False)
def load_model(path="model.pkl"):
    return joblib.load(path)

try:
    model = load_model("model.pkl")
except Exception as e:
    st.error(f"Failed to load `model.pkl`. Details: {e}")
    st.info("Confirm scikit-learn/joblib versions match those used when saving the model.")
    st.stop()

vaccine_map = {"Covaxin": 0, "Covishield": 1, "Pfizer": 2, "None": 3}

with st.form("risk_form"):
    st.subheader("🧑‍⚕️ Basic Health Information")
    age = st.number_input("🎂 Age", 10, 100, 40)
    resting_bp = st.number_input("🩺 Resting Blood Pressure", 80, 200, 120)
    cholesterol = st.number_input("🧬 Cholesterol Level (mg/dL)", 100, 400, 200)
    max_hr = st.number_input("❤️ Max Heart Rate Achieved", 60, 220, 150)

    st.subheader("📋 Medical History")
    diabetes = st.radio("🩸 Do you have Diabetes?", ["No", "Yes"], horizontal=True)
    hypertension = st.radio("💥 Do you have Hypertension?", ["No", "Yes"], horizontal=True)
    heart_condition = st.radio("❤️ Do you have any Heart Condition?", ["No", "Yes"], horizontal=True)

    st.subheader("🦠 COVID-Related Info")
    vaccinated = st.radio("💉 Are you Vaccinated against COVID?", ["No", "Yes"], horizontal=True)
    hospitalized = st.radio("🏥 Were you hospitalized due to COVID?", ["No", "Yes"], horizontal=True)
    vaccine_type = st.selectbox("🧪 Which vaccine did you receive?", list(vaccine_map.keys()))
    doses = st.number_input("💉 Number of Vaccine Doses Received", 0, 5, 2)
    days_since_vaccine = st.number_input("📅 Days Since Last Vaccine Dose", 0, 365, 60)

    submit = st.form_submit_button("🔍 Predict My Risk")

if submit:
    # Ensure feature order matches the trained model
    row = {
        "Age": age,
        "RestingBP": resting_bp,
        "Cholesterol": cholesterol,
        "MaxHR": max_hr,
        "Diabetes": 1 if diabetes == "Yes" else 0,
        "Hypertension": 1 if hypertension == "Yes" else 0,
        "Heart_Condition": 1 if heart_condition == "Yes" else 0,
        "Vaccinated": 1 if vaccinated == "Yes" else 0,
        "Hospitalized": 1 if hospitalized == "Yes" else 0,
        "Vaccine_Type": vaccine_map[vaccine_type],
        "Doses": doses,
        "Days_Since_Vaccine": days_since_vaccine
    }

    if hasattr(model, "feature_names_in_"):
        input_df = pd.DataFrame([row], columns=model.feature_names_in_)
    else:
        input_df = pd.DataFrame([row])

    prob = float(model.predict_proba(input_df)[0][1])
    pred = 1 if prob > 0.5 else 0

    if prob > 0.75:
        tier, coverage, premium = "🚨 Premium", "₹2 – ₹5 Lakh", "₹10,000+"
    elif prob > 0.4:
        tier, coverage, premium = "⚠️ Standard", "₹5 – ₹10 Lakh", "₹6,000 – ₹9,000"
    else:
        tier, coverage, premium = "✅ Basic", "₹10 – ₹15 Lakh", "₹4,000 – ₹6,000"

    if pred == 1:
        st.markdown(f"""
        <div style='background:#ffe5e5;padding:20px;border-radius:10px;text-align:center;'>
            <h2 style='color:red;'>⚠️ High Risk</h2>
            <p>Risk Score: <strong>{prob:.2f}</strong>. Please consult a doctor.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='background:#e6ffed;padding:20px;border-radius:10px;text-align:center;'>
            <h2 style='color:green;'>✅ Low Risk</h2>
            <p>Risk Score: <strong>{prob:.2f}</strong></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:#f1f3f6;padding:20px;border-radius:10px;'>
      <h3>🛡 Recommended Insurance Plan</h3>
      <ul>
        <li><strong>Policy Tier:</strong> {tier}</li>
        <li><strong>Coverage:</strong> {coverage}</li>
        <li><strong>Estimated Premium:</strong> {premium}</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    out = dict(row)
    out.update({
        "Risk_Score": prob,
        "Prediction": pred,
        "Tier": tier,
        "Coverage": coverage,
        "Premium": premium
    })
    save_history(email, out)
