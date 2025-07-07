import streamlit as st
import pandas as pd
import joblib
import os

# Load trained model
model = joblib.load("model.pkl")

# Streamlit page setup
#st.set_page_config(page_title="Post-COVID Heart Risk Predictor", page_icon="💓", layout="centered")

# Header
st.markdown("""
    <h1 style='text-align: center; color: #d6336c;'>💓 Post-COVID Heart Risk Predictor</h1>
    <p style='text-align: center; font-size: 18px; color: #555;'>Check if you are at risk of heart-related complications after COVID-19.</p>
    <hr style='border: 1px solid #eee;' />
""", unsafe_allow_html=True)

# Input Form
with st.form("risk_form"):
    st.subheader("🧑‍⚕️ Basic Health Information")
    age = st.number_input("🎂 Age", min_value=10, max_value=100, value=40)
    resting_bp = st.number_input("🩺 Resting Blood Pressure", min_value=80, max_value=200, value=120)
    cholesterol = st.number_input("🧬 Cholesterol Level (mg/dL)", min_value=100, max_value=400, value=200)
    max_hr = st.number_input("❤️ Max Heart Rate Achieved", min_value=60, max_value=220, value=150)

    st.subheader("📋 Medical History")
    diabetes = st.radio("🩸 Do you have Diabetes?", ["No", "Yes"], horizontal=True)
    hypertension = st.radio("💥 Do you have Hypertension?", ["No", "Yes"], horizontal=True)
    heart_condition = st.radio("❤️ Do you have any Heart Condition?", ["No", "Yes"], horizontal=True)

    st.subheader("🦠 COVID-Related Info")
    vaccinated = st.radio("💉 Are you Vaccinated against COVID?", ["No", "Yes"], horizontal=True)
    hospitalized = st.radio("🏥 Were you hospitalized due to COVID?", ["No", "Yes"], horizontal=True)
    vaccine_type = st.selectbox("🧪 Which vaccine did you receive?", ["Covaxin", "Covishield", "Pfizer", "None"])

    submit = st.form_submit_button("🔍 Predict My Risk")

# Prediction Logic
if submit:
    # Encode inputs
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
        "Vaccine_Type": {"Covaxin": 0, "Covishield": 1, "Pfizer": 2, "None": 3}[vaccine_type]
    }])

    # Make prediction
    prediction = model.predict(input_data)[0]

    st.markdown("<br>", unsafe_allow_html=True)

    if prediction == 1:
        st.markdown("""
            <div style='background-color: #ffe5e5; padding: 20px; border-radius: 10px; text-align: center;'>
                <h2 style='color: red;'>⚠️ High Risk</h2>
                <p>You may be at <strong>high risk</strong> for heart issues post COVID. Please consult a doctor.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='background-color: #e6ffed; padding: 20px; border-radius: 10px; text-align: center;'>
                <h2 style='color: green;'>✅ Low Risk</h2>
                <p>You are likely at <strong>low risk</strong>. Stay healthy and monitor your symptoms regularly.</p>
            </div>
        """, unsafe_allow_html=True)

    # SHAP Summary (if file exists)
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📊 Show Feature Importance (SHAP Summary Plot)", expanded=False):
        if os.path.exists("shap_summary.png"):
            st.image("shap_summary.png", caption="SHAP summary of feature impact on heart risk prediction", use_column_width=True)
        else:
            st.warning("SHAP summary not available. Please re-run the training script to generate it.")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("🔬 Built with ❤️ using Streamlit • Stay safe, stay informed.")
