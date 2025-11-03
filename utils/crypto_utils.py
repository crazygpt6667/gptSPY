"""
Cryptographic Utilities for Secure File Communication Application
"""

import os
import base64
# Optional import no longer needed with Python 3.10+ union syntax
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class CryptoUtils:
    """Utility class for cryptographic operations"""
    
    @staticmethod
    def generate_key() -> bytes:
        """Generate a new Fernet key"""
        return Fernet.generate_key()
        
    @staticmethod
    def derive_key_from_password(password: str, salt: bytes | None = None) -> tuple[bytes, bytes]:
        """
        Derive a key from a password using PBKDF2
        
        Args:
            password (str): Password to derive key from
            salt (bytes): Salt for key derivation (generated if None)
            
        Returns:
            tuple: (key, salt) - Derived key and salt used
        """
        if salt is None:
            salt = os.urandom(16)
            
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
        
    @staticmethod
    def encrypt_data(data: str, key: bytes) -> str:
        """
        Encrypt data using Fernet encryption
        
        Args:
            data (str): Data to encrypt
            key (bytes): Encryption key
            
        Returns:
            str: Base64-encoded encrypted data
        """
        cipher_suite: Fernet = Fernet(key)
        encrypted_data = cipher_suite.encrypt(data.encode())
        return base64.b64encode(encrypted_data).decode()
        
    @staticmethod
    def decrypt_data(encrypted_data: str, key: bytes) -> str:
        """
        Decrypt data using Fernet encryption
        
        Args:
            encrypted_data (str): Base64-encoded encrypted data
            key (bytes): Decryption key
            
        Returns:
            str: Decrypted data
        """
        cipher_suite: Fernet = Fernet(key)
        encrypted_bytes = base64.b64decode(encrypted_data.encode())
        decrypted_data = cipher_suite.decrypt(encrypted_bytes)
        return decrypted_data.decode()