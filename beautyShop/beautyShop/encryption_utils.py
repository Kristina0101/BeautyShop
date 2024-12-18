from cryptography.fernet import Fernet
from django.conf import settings

# Создаём объект шифрования
fernet = Fernet(settings.ENCRYPTION_KEY)

def encrypt_data(data: str) -> str:
    if not data:
        return None
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(data: str) -> str:
    if not data:
        return None
    return fernet.decrypt(data.encode()).decode()
