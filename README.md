# 💓 CardioCare AI 

An AI-powered **post-COVID health screening tool** built with **Streamlit**, integrating:

- 🔍 **Heart risk prediction** using machine learning (Random Forest)
- 🫁 **Lung imaging (beta)** — chest X-ray opacity detection
- 🔐 **Login / Sign up system** with user history tracking
- 📊 **Insurance estimator** (experimental) based on predicted risk

[Try it here](https://cardiocare-ai.streamlit.app/) 

⚠️ **Disclaimer:** This project is for **research and educational purposes only**.  
It is **not a medical device** and should not be used as a substitute for professional medical advice.

---

## ✨ Features

### 🔐 Login / Sign Up
- User authentication with email and password
- Session-based login using Streamlit state
- Saves user prediction history

### 🔍 Heart Risk Prediction
- Inputs: Age, Blood Pressure, Cholesterol, Max Heart Rate
- Medical history: Diabetes, Hypertension, Heart Condition
- COVID-19 details: Vaccination, Hospitalization, Vaccine type, Doses
- **Output**: Risk score (0–1), risk category (High/Low), recommended insurance tier

### 🫁 Imaging (beta): Chest X-ray Analysis
- Upload **PNG/JPG/DICOM** chest X-rays
- Automatic lung segmentation + preprocessing
- Highlights potential **post-COVID opacities** (ground-glass, consolidations)
- Adjustable detection settings:
  - Threshold method: **Z-score** or **Percentile**
  - Sensitivity control
  - Mask padding (peripheral inclusion)
  - Minimum region size filter
- Outputs:
  - % of lung affected
  - Affected pixel counts
  - Downloadable overlay PNG with opacity heatmap

### 📖 About Page
- Information on post-COVID cardiovascular risk
- Vaccine effects (simulated data)
- Lifestyle tips & follow-up guidelines
- Future roadmap for enhancements

---

## 🛠 Tech Stack

- **Frontend/UI**: [Streamlit](https://streamlit.io/)
- **ML Model**: Scikit-learn (Random Forest Classifier, joblib for persistence)
- **Image Processing**: OpenCV, scikit-image, pydicom
- **Database**: SQLite (lightweight user + history storage)
- **Language**: Python 3.12+

---

## 📂 Project Structure

```

heart-risk-app/
│
├── Home.py                  # Entry point
├── utils/
│   └── db\_manager.py        # Database setup & helpers
├── pages/
│   ├── 0\_Login.py           # Login / Sign up
│   ├── 1\_Predict.py         # Heart risk prediction
│   ├── 2\_Imaging\_Beta\_CXR.py# Lung imaging (beta)
│   └── 3\_About.py           # About page
├── model.pkl                # Trained Random Forest model
├── requirements.txt         # Dependencies
└── README.md                # Project documentation

````

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/gayatrinagi/CoronaShield-HeartCare.git
cd CoronaShield-HeartCare
````

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
.\venv\Scripts\activate   # on Windows
source venv/bin/activate  # on Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run Home.py
```

---

## 📸 Screenshots (to be added)

* Login Page
* Risk Prediction Page
* Imaging (beta) with X-ray overlay

---

## 🛡 Disclaimer

This app is for **research/educational awareness** only.
It does **not provide medical advice**. Please consult a healthcare professional for any medical concerns.

---

## 👩‍💻 Author

Built by **Gayatri Nagi**
🔗 GitHub: [gayatrinagi](https://github.com/gayatrinagi)

---

## 🔮 Future Enhancements

* SHAP explainability (feature importance visualization)
* PDF report export
* User health dashboard
* Improved lung segmentation (deep learning U-Net)
* API backend for mobile/remote integration


