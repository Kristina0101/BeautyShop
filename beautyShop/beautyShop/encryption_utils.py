from cryptography.fernet import Fernet, InvalidToken
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
    try:
        decrypted = fernet.decrypt(data.encode()).decode()
        print(f"Дешифруем: {data} -> {decrypted}")
        return decrypted
    except InvalidToken:
        raise ValueError("Неверный ключ шифрования или повреждённые данные")