import hashlib
import secrets


def hash_password(password: str, password_salt: str) -> str:
    return hashlib.sha256((password + password_salt).encode()).hexdigest()


def check_password(password: str, password_hash: str, password_salt: str) -> bool:
    return hash_password(password, password_salt) == password_hash


def generate_salt() -> str:
    return secrets.token_hex(16)


def generate_password_hash(password: str) -> (str, str):
    password_salt = generate_salt()
    password_hash = hash_password(password, password_salt)
    return password_hash, password_salt
