import sqlite3
import datetime
import hashlib

DB_PATH = "user_history.db"

def init_user_db():
    print("Initializing user DB...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password_hash TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("User DB initialized.")

def init_db():
    print("Initializing prediction history DB...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            timestamp TEXT,
            Age INTEGER,
            RestingBP INTEGER,
            Cholesterol INTEGER,
            MaxHR INTEGER,
            Diabetes INTEGER,
            Hypertension INTEGER,
            Heart_Condition INTEGER,
            Vaccinated INTEGER,
            Hospitalized INTEGER,
            Vaccine_Type INTEGER,
            Risk_Score REAL,
            Prediction INTEGER,
            Tier TEXT,
            Coverage TEXT,
            Premium TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Prediction history DB initialized.")

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(email: str, password: str) -> bool:
    print(f"Creating user: {email}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (email, password_hash, created_at)
            VALUES (?, ?, ?)
        """, (email.strip().lower(), hash_password(password), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        print(f"User {email} created successfully.")
        return True
    except sqlite3.IntegrityError:
        print(f"User {email} already exists.")
        return False  # Email already exists
    finally:
        conn.close()

def authenticate_user(email: str, password: str) -> bool:
    email = email.strip().lower()
    print(f"Authenticating user: {email}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    if row:
        print(f"User found. Stored hash: {row[0]}")
    else:
        print("User not found.")
    if row and row[0] == hash_password(password):
        print("Password match. Authentication successful.")
        return True
    else:
        print("Password mismatch or user not found. Authentication failed.")
        return False

def save_history(email, data):
    print(f"Saving history for {email}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO prediction_history (
            email, timestamp, Age, RestingBP, Cholesterol, MaxHR,
            Diabetes, Hypertension, Heart_Condition, Vaccinated,
            Hospitalized, Vaccine_Type, Risk_Score, Prediction,
            Tier, Coverage, Premium
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        email, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data["Age"], data["RestingBP"], data["Cholesterol"], data["MaxHR"],
        data["Diabetes"], data["Hypertension"], data["Heart_Condition"],
        data["Vaccinated"], data["Hospitalized"], data["Vaccine_Type"],
        data["Risk_Score"], data["Prediction"], data["Tier"],
        data["Coverage"], data["Premium"]
    ))
    conn.commit()
    conn.close()
    print(f"History saved for {email}")

def get_user_history(email):
    print(f"Fetching history for {email}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prediction_history WHERE email = ? ORDER BY timestamp DESC", (email,))
    rows = cursor.fetchall()
    conn.close()
    return rows
