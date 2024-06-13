from cryptography.fernet import Fernet
from django.conf import settings

class CryptoManager:
    def __init__(self):
        self.key = settings.ENCRYPTION_KEY.encode()  # Ключ должен быть в байтовом формате
        self.cipher_suite = Fernet(self.key)

    def encrypt(self, text: str):
        return self.cipher_suite.encrypt(text.encode()).decode()

    def decrypt(self, encrypted_text: str):
        return self.cipher_suite.decrypt(encrypted_text.encode()).decode()