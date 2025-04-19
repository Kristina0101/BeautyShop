from cryptography.fernet import Fernet
from django.conf import settings

fernet = Fernet(settings.ENCRYPTION_KEY)

def encrypt_data(data: str) -> str:
    if not data:
        return None
    encrypted = fernet.encrypt(data.encode()).decode()
    print(f"Шифруем: {data} -> {encrypted}")
    return encrypted


def decrypt_data(data: str) -> str:
    if not data:
        return None
    return fernet.decrypt(data.encode()).decode()
