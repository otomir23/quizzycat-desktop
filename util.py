import hashlib
import os
import secrets
import sys


def hash_password(password: str, password_salt: str) -> str:
    """Hashes a password with a salt using SHA-256."""
    return hashlib.sha256((password + password_salt).encode()).hexdigest()


def check_password(password: str, password_hash: str, password_salt: str) -> bool:
    """Checks if a password matches a hash and salt."""
    return hash_password(password, password_salt) == password_hash


def generate_salt() -> str:
    """Generates a random salt."""
    return secrets.token_hex(16)


def generate_password_hash(password: str) -> (str, str):
    """Generates a random salt and hashes a password with it."""
    password_salt = generate_salt()
    password_hash = hash_password(password, password_salt)
    return password_hash, password_salt


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
