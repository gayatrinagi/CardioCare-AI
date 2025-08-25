# pages/0_Login.py
import streamlit as st
from utils.db_manager import init_user_db, init_db, create_user, authenticate_user

# init (idempotent)
init_user_db()
init_db()

st.title("🔐 Login or Sign Up")

form_type = st.radio("Choose an action:", ["Login", "Sign Up"], horizontal=True)
email = st.text_input("Email")
password = st.text_input("Password", type="password")

# Ensure session keys exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "email" not in st.session_state:
    st.session_state.email = ""

if form_type == "Sign Up":
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Sign Up"):
        if not email or not password or not confirm_password:
            st.error("Please fill in all fields.")
        elif password != confirm_password:
            st.error("❌ Passwords do not match.")
        else:
            ok = create_user(email.strip().lower(), password)
            if ok:
                st.success("✅ Account created! Please login.")
            else:
                st.error("❌ Email already exists. Try logging in.")
else:
    if st.button("Login"):
        if not email or not password:
            st.error("Please enter both email and password.")
        else:
            ok = authenticate_user(email.strip().lower(), password)
            if ok:
                st.session_state.logged_in = True
                st.session_state.email = email.strip().lower()
                st.success("✅ Login successful! Go to **Predict** or **Imaging (beta)** from the sidebar.")
                st.page_link("pages/1_Predict.py", label="→ Open Predict page")
            else:
                st.error("❌ Invalid email or password.")
