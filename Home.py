import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "email" not in st.session_state:
    st.session_state.email = ""

st.set_page_config(
    page_title="CardioCare AI",
    page_icon="💓",
    layout="centered",
)

# === Custom Banner ===
col1, col2 = st.columns([1, 6])
with col1:
    st.image("logo.png", width=60)  # Replace with your actual logo
with col2:
    st.markdown("""
        <h1 style='color:#d6336c; margin-bottom:0;'>CardioCare AI</h1>
        <p style='margin-top:0; color:#666;'>AI-powered heart health screening after COVID-19</p>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# === App Intro ===
st.markdown("""
Welcome to **CardioCare AI**, a smart risk assessment tool built to help users detect potential **heart-related complications** after recovering from COVID-19.

Use the **sidebar** to:
- 🔍 Predict your risk
- 📊 Understand model explanations (SHAP)
- 📖 Learn more about the science behind it
""")

st.markdown("💡 This app is for awareness purposes and does not replace medical advice.")

st.markdown("---")

# === Feature Image (Optional) ===
st.image("images/heart-health.png", caption="Stay informed. Stay healthy.", use_column_width=True)
