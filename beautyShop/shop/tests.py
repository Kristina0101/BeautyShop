from django.test import TestCase

from users.models import CustomUser

# Create your tests here.

user = CustomUser.objects.create()
user.email = "test@example.com"
user.save()

print(user.encrypted_email)  # Увидите зашифрованный текст
print(user.email)  # Увидите "test@example.com"

