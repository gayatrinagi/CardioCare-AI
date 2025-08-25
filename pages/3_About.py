# pages/3_About.py
import streamlit as st

st.set_page_config(page_title="About • CardioCare AI", page_icon="💓", layout="centered")

st.title("📖 About CardioCare AI")

st.markdown("""
CardioCare AI is a **health awareness** app that helps users:
1) **Estimate post-COVID heart risk** using a machine-learning model, and  
2) **Visualize lung opacities on X-rays (Imaging • beta)** using image processing.

> ⚠️ This app is **not** a medical device and does **not** provide a diagnosis. Results are for **education and awareness only**. Please consult a qualified clinician for clinical use.
""")

st.markdown("---")

st.header("💓 Post-COVID Heart Risk (Predict)")
st.markdown("""
- **What it does:** Uses features like Age, Blood Pressure, Cholesterol, Diabetes/Hypertension history, Vaccination, etc., to estimate a probability of heart-related complications post-COVID.
- **Model (current):** `RandomForestClassifier` (loaded from `model.pkl`).
- **Output:** Risk score (0–1), **High/Low Risk** tag, and a **sample insurance tier** suggestion (for demo).
- **Explainability:** You can add SHAP plots later to explain per-feature contributions.
""")

st.markdown("**Try it:**")
st.page_link("pages/1_Predict.py", label="🔍 Open Predict page")

st.markdown("---")

st.header("🫁 Lung Imaging (beta): X-ray Opacity Overlay")
st.markdown("""
- **Goal:** Help users **see potential bright opacities** (e.g., ground-glass, consolidation) that are sometimes associated with **post-COVID** changes.
- **Inputs:** Chest X-ray in **PNG/JPG** or **DICOM (.dcm)**.
- **Pipeline (heuristic; no AI diagnosis):**
  1. **Preprocess**: Resize → CLAHE contrast → Denoise  
  2. **Lung mask**: OpenCV threshold + morphology to isolate lungs  
  3. **Opacity map**: Z-score brightness **inside the lung mask** and highlight bright regions  
  4. **Overlay**: Color heatmap on the original image  
  5. **Metrics**: % lung affected, left vs right, **peripheral** and **lower-zone** shares

- **What the numbers mean:**
  - **% Lung affected** — rough area of bright regions; higher can suggest more extensive opacities.
  - **Peripheral predominance** — post-COVID patterns are often peripheral; high % may be consistent.
  - **Lower-zone share** — some viral patterns favor lower lobes.
  - **These are heuristics**; bones/exposure/artifacts can trigger false highlights.
""")

st.markdown("**Try it:**")
st.page_link("pages/2_Imaging_Beta_CXR.py", label="🫁 Open Imaging (beta)")

st.markdown("> 💡 You can **download** the overlay PNG for documentation. For cleaner borders, you may later swap the quick lung mask for a **U-Net** segmentation, or add a small **CNN** + Grad-CAM.")

st.markdown("---")

st.header("🔐 Data & Privacy")
st.markdown("""
- Uploaded images are processed **in memory** by Streamlit; **no cloud uploads** are performed unless you add logging/storage.
- Do **not** use this app for real patient care without appropriate approvals and safeguards.
""")

st.markdown("---")

st.header("🧪 Model & Features (summary)")
st.markdown("""
- **Classifier:** Random Forest (`model.pkl`)
- **Features (examples):** Age, RestingBP, Cholesterol, MaxHR, Diabetes, Hypertension, Heart Condition, COVID hospitalization, Vaccination (type/doses/days).
- **Vaccine feature mapping:** Covaxin=0, Covishield=1, Pfizer=2, None=3.
- **Output:** Risk Score → Tier suggestion (**demo only**).
""")

st.markdown("---")

st.header("⚙️ How to Run (local)")
st.code("py -m streamlit run Home.py", language="bash")
st.markdown("""
- Open the link shown in the terminal (usually **http://localhost:8501**).
- Navigate via the left sidebar: **Home → 0_Login → 1_Predict → 2_Imaging_Beta_CXR**.
""")

st.markdown("**Quick links:**")
cols = st.columns(3)
with cols[0]:
    st.page_link("Home.py", label="🏠 Home")
with cols[1]:
    st.page_link("pages/0_Login.py", label="🔐 Login / Sign Up")
with cols[2]:
    st.page_link("pages/1_Predict.py", label="🔍 Predict")
st.page_link("pages/2_Imaging_Beta_CXR.py", label="🫁 Imaging (beta)")

st.markdown("---")

st.header("🧩 Requirements (core)")
st.code(
"""streamlit>=1.36
numpy>=1.26
pillow>=10.0
joblib>=1.4
scikit-learn>=1.5
opencv-python-headless>=4.9
pydicom>=2.4
scikit-image>=0.24
""", language="text")

st.markdown("---")

st.header("🧯 Troubleshooting")
st.markdown("""
- **App doesn’t open** → Always run with: `py -m streamlit run Home.py`
- **ModuleNotFoundError** → Install requirements: `py -m pip install -r requirements.txt`
- **Different Python versions** → Ensure install + run use the **same** interpreter (`py --version`)
- **Page not found** → Files must live in **`pages/`** with the exact names (e.g., `pages/0_Login.py`).
- **Imaging missing** → Install: `py -m pip install opencv-python-headless pydicom scikit-image`
- **Deprecation** → Use `use_container_width=True` (not `use_column_width`).
""")

st.markdown("---")

st.header("🚀 Roadmap")
st.markdown("""
- U-Net lung segmentation (cleaner masks)  
- CNN-based opacity scoring + **Grad-CAM** heatmaps  
- Per-user dashboards & PDF report export  
- API endpoint for mobile/partner integration  
""")

st.markdown("---")

st.header("🙌 Credits")
st.markdown("""
Built by **Nagig** • Stack: Streamlit • scikit-learn • OpenCV • pydicom • scikit-image  
""")
