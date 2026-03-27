from passlib.context import CryptContext
import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "admin123"
print(f"Testing password: {password}")

try:
    hashed = pwd_context.hash(password)
    print(f"Hashed with passlib: {hashed}")
except Exception as e:
    print(f"Passlib hashing failed: {e}")

try:
    salt = bcrypt.gensalt()
    hashed_bcrypt = bcrypt.hashpw(password.encode('utf-8'), salt)
    print(f"Hashed with direct bcrypt: {hashed_bcrypt}")
except Exception as e:
    print(f"Direct bcrypt hashing failed: {e}")
