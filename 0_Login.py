import streamlit as st
from utils.db_manager import init_user_db, init_db, create_user, authenticate_user

# Initialize DBs
init_user_db()
init_db()

st.set_page_config(page_title="Login / Sign Up", layout="centered")
st.title("🔐 Login or Sign Up")

form_type = st.radio("Choose an action:", ["Login", "Sign Up"], horizontal=True)

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if form_type == "Sign Up":
    confirm_password = st.text_input("Confirm Password", type="password")
    signup_clicked = st.button("Sign Up")

    if signup_clicked:
        if not email or not password or not confirm_password:
            st.error("Please fill in all fields.")
        elif password != confirm_password:
            st.error("❌ Passwords do not match.")
        else:
            success = create_user(email.strip().lower(), password)
            if success:
                st.success("✅ Account created successfully! Please login.")
            else:
                st.error("❌ Email already exists. Try logging in.")

elif form_type == "Login":
    login_clicked = st.button("Login")

    if login_clicked:
        if not email or not password:
            st.error("Please enter both email and password.")
        else:
            authenticated = authenticate_user(email.strip().lower(), password)
            if authenticated:
                #st.success("✅ Login successful!")
                st.session_state.logged_in = True
                st.session_state.email = email.strip().lower()
    
                st.success("✅ Login successful! Please select 'Prediction' page from sidebar.")

                
            else:
                st.error("❌ Invalid email or password.")
