import streamlit as st
import pandas as pd
import joblib
from utils.db_manager import save_history  # Make sure this path is correct

# Load model
model = joblib.load("model.pkl")

vaccine_map = {"Covaxin": 0, "Covishield": 1, "Pfizer": 2, "None": 3}

st.title("🔍 Post-COVID Heart Risk & Insurance Estimator")

if not st.session_state.get("logged_in", False):
    st.warning("🔒 Please log in to access the prediction tool.")
    st.stop()

email = st.session_state.get("email", "guest@demo.com")

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
    input_data = pd.DataFrame([{
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
    }], columns=model.feature_names_in_)  # enforce order and names

    

    risk_score = model.predict_proba(input_data)[0][1]
    prediction = 1 if risk_score > 0.5 else 0

    if risk_score > 0.75:
        tier = "🚨 Premium"
        coverage = "₹2 – ₹5 Lakh"
        premium = "₹10,000+"
    elif risk_score > 0.4:
        tier = "⚠️ Standard"
        coverage = "₹5 – ₹10 Lakh"
        premium = "₹6,000 – ₹9,000"
    else:
        tier = "✅ Basic"
        coverage = "₹10 – ₹15 Lakh"
        premium = "₹4,000 – ₹6,000"

    if prediction == 1:
        st.markdown(f"""
            <div style='background-color: #ffe5e5; padding: 20px; border-radius: 10px; text-align: center;'>
                <h2 style='color: red;'>⚠️ High Risk</h2>
                <p>Your heart risk after COVID is high. Risk Score: <strong>{risk_score:.2f}</strong><br>
                Please consult a doctor immediately.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style='background-color: #e6ffed; padding: 20px; border-radius: 10px; text-align: center;'>
                <h2 style='color: green;'>✅ Low Risk</h2>
                <p>You are likely at low risk. Risk Score: <strong>{risk_score:.2f}</strong></p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <br>
    <div style='background-color:#f1f3f6; padding:20px; border-radius:10px;'>
        <h3>🛡 Recommended Insurance Plan</h3>
        <ul>
            <li><strong>Policy Tier:</strong> {tier}</li>
            <li><strong>Coverage Level:</strong> {coverage}</li>
            <li><strong>Estimated Premium:</strong> {premium}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    save_data = input_data.iloc[0].to_dict()

# Ensure these keys exist in save_data (sometimes they may get lost if columns mismatch)
    save_data["Risk_Score"] = risk_score
    save_data["Prediction"] = prediction
    save_data["Tier"] = tier
    save_data["Coverage"] = coverage
    save_data["Premium"] = premium

# Also explicitly add doses and days since vaccine from your variables:
    save_data["Doses"] = doses
    save_data["Days_Since_Vaccine"] = days_since_vaccine




    save_history(email, save_data)
