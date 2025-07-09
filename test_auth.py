import hashlib

print("Starting test_auth script")

from utils.db_manager import authenticate_user, hash_password

print("Imported authenticate_user")

email = "nagi.gayatri@gmail.com"  # Use your exact signup email
password = "1234"          # Use your exact signup password

print(f"Authenticating user: '{email}' with password: '{password}'")
print(f"Password SHA256 hash: {hash_password(password)}")

result = authenticate_user(email, password)

print(f"Result: {result}")

if result:
    print("Login success!")
else:
    print("Login failed!")
