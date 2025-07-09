import sqlite3

def list_users():
    conn = sqlite3.connect("user_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT email, password_hash FROM users")
    users = cursor.fetchall()
    conn.close()

    print("Users in DB:")
    if not users:
        print("No users found.")
    else:
        for email, pw_hash in users:
            print(f"Email: {email}, Password Hash: {pw_hash}")

if __name__ == "__main__":
    list_users()
