import streamlit as st
import pandas as pd
from utils.db_manager import get_user_history, init_db


# Initialize database
init_db()

st.set_page_config(page_title="Prediction History", layout="centered")

st.title("📜 Prediction History")

# Simulated logged-in user (replace with session-based logic later)
email = "admin@demo.com"

# Get user prediction history
history = get_user_history(email)

if not history:
    st.info("No prediction history found.")
else:
    # Convert to DataFrame
    columns = [
    "ID", "Email", "Timestamp", "Age", "RestingBP", "Cholesterol", "MaxHR",
    "Diabetes", "Hypertension", "Heart_Condition", "Vaccinated",
    "Hospitalized", "Vaccine_Type", "Doses", "Days_Since_Vaccine",
    "Risk_Score", "Prediction", "Tier", "Coverage", "Premium"
]

    df = pd.DataFrame(history, columns=columns)
    st.dataframe(df.drop(columns=["ID", "Email"]), use_container_width=True)


    # Export option
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download History as CSV", data=csv, file_name="my_predictions.csv", mime="text/csv")
