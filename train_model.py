import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

print("📦 Loading enhanced dataset...")

df = pd.read_csv("enhanced_dataset.csv")

# Map vaccine types
vaccine_map = {"Covaxin": 0, "Covishield": 1, "Pfizer": 2, "None": 3}
df["Vaccine_Type"] = df["Vaccine_Type"].map(vaccine_map)

# Add synthetic features if missing
if "Doses" not in df.columns:
    np.random.seed(42)
    df["Doses"] = np.random.randint(0, 4, size=len(df))
if "Days_Since_Vaccine" not in df.columns:
    df["Days_Since_Vaccine"] = np.random.randint(0, 365, size=len(df))

features = [
    "Age", "RestingBP", "Cholesterol", "MaxHR",
    "Diabetes", "Hypertension", "Heart_Condition",
    "Vaccinated", "Hospitalized", "Vaccine_Type",
    "Doses", "Days_Since_Vaccine"
]

X = df[features]
y = df["Target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, "model.pkl")
print("✅ Model retrained and saved as model.pkl")
print("Model feature names:", model.feature_names_in_)
