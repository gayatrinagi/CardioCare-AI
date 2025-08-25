# Home.py — CardioCare AI (Refreshed Home)
import streamlit as st

st.set_page_config(page_title="CardioCare AI", page_icon="💓", layout="centered")

# =========================
# Header / Banner
# =========================
col1, col2 = st.columns([1, 7])
with col1:
    st.image("logo.png", width=56)
with col2:
    st.markdown("""
        <h1 style='color:#d6336c; margin:0;'>CardioCare AI</h1>
        <p style='margin:2px 0 0 0; color:#666; font-size:16px;'>
            AI-powered post-COVID heart-risk screening & lung imaging (beta)
        </p>
    """, unsafe_allow_html=True)

st.markdown("<hr style='margin-top:12px;'>", unsafe_allow_html=True)

# =========================
# Intro
# =========================
st.markdown("""
Welcome to **CardioCare AI** — a research/education app that helps you:

- **Estimate post-COVID heart risk** using a machine-learning model (demo).
- **Visualize possible opacities** on chest X-rays (🫁 *Imaging — beta*).
  
> ⚠️ **Not a medical device**. Results are heuristic and must not be used for diagnosis. Always consult a clinician.
""")

# =========================
# Quick Access Cards
# =========================
st.markdown("### Quick access")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div style="
            background:#fff;
            border:1px solid #eee;
            border-radius:14px;
            padding:16px;
            box-shadow:0 1px 6px rgba(0,0,0,0.05);
            height:100%;
        ">
            <h4 style="margin:0 0 8px 0;">🔐 Login / Sign Up</h4>
            <p style="color:#555; margin:0 0 12px 0;">
                Create an account or sign in to enable predictions and imaging.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/0_Login.py", label="Open Login / Sign Up")

with c2:
    st.markdown(
        """
        <div style="
            background:#fff;
            border:1px solid #eee;
            border-radius:14px;
            padding:16px;
            box-shadow:0 1px 6px rgba(0,0,0,0.05);
            height:100%;
        ">
            <h4 style="margin:0 0 8px 0;">🔍 Predict Risk</h4>
            <p style="color:#555; margin:0 0 12px 0;">
                Enter basic health & COVID details to get a risk score and a demo insurance tier.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/1_Predict.py", label="Open Predict")

with c3:
    st.markdown(
        """
        <div style="
            background:#fff;
            border:1px solid #eee;
            border-radius:14px;
            padding:16px;
            box-shadow:0 1px 6px rgba(0,0,0,0.05);
            height:100%;
        ">
            <h4 style="margin:0 0 8px 0;">🫁 Imaging (beta)</h4>
            <p style="color:#555; margin:0 0 12px 0;">
                Upload a chest X-ray (PNG/JPG/DICOM). See a color overlay of bright opacities with simple metrics.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/2_Imaging_Beta_CXR.py", label="Open Imaging (beta)")

st.markdown("---")

# =========================
# What you can do
# =========================
st.markdown("### What you can do here")
st.markdown(
"""
- **Risk Estimation:** Get a probability and a **High/Low** tag based on features like Age, BP, Cholesterol, Diabetes/Hypertension, Vaccination, etc.  
- **Lung Imaging (beta):** 
  - Preprocess (CLAHE, denoise) → **Lung mask** (OpenCV) → **Brightness-based overlay** inside the mask  
  - **Metrics:** % lung affected, left vs right, **peripheral** and **lower-zone** predominance  
  - **Download** the overlay PNG for your notes
- **Account-based history** (if you enabled it in your DB layer) to save prediction inputs & results.
"""
)

# =========================
# How it works (concise)
# =========================
with st.expander("🧠 How it works (concise)"):
    st.markdown(
        """
        **Predict:**  
        - Loads a `RandomForestClassifier` from `model.pkl` (**demo**); you can swap in your trained model.  
        - Uses structured inputs (age, BP, etc.) → **risk score** & tier suggestion (for awareness).  

        **Imaging (beta):**  
        - OpenCV & scikit-image pipeline (no diagnostic AI):  
          1) Preprocess (resize, CLAHE, denoise)  
          2) Quick **lung segmentation** (threshold + morphology)  
          3) **Z-score** brightness inside lungs → highlight bright areas  
          4) Show overlay + metrics  

        > This is a heuristic visualization. Ribs/artifacts/exposure can trigger false highlights.
        """
    )

# =========================
# Helpful links & tips
# =========================
st.markdown("### Helpful links & tips")
t1, t2 = st.columns(2)
with t1:
    st.markdown(
        """
        - First time? **Login/Sign Up** → then open **Predict** / **Imaging**  
        - Run locally with:
        """
    )
    st.code("py -m streamlit run Home.py", language="bash")
with t2:
    st.markdown(
        """
        - If a page doesn’t appear: make sure files are inside the **`pages/`** folder  
        - If modules are missing:
        """
    )
    st.code("py -m pip install -r requirements.txt", language="bash")

# =========================
# Footer / Disclaimer
# =========================
st.markdown("---")
st.markdown(
    """
    <div style="color:#666; font-size:13px;">
        Built for awareness and education — not for diagnosis. Always consult a clinician for medical advice.
    </div>
    """,
    unsafe_allow_html=True,
)
