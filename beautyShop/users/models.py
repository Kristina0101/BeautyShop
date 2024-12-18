from django.contrib.auth.models import User
from django.db import models
from beautyShop.encryption_utils import encrypt_data, decrypt_data


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile/%Y/%m/%d')
    encrypted_phone = models.TextField(blank=True, null=True)

    @property
    def phone(self):
        return decrypt_data(self.encrypted_phone) if self.encrypted_phone else None

    @phone.setter
    def phone(self, value):
        self.encrypted_phone = encrypt_data(value)

    def __str__(self):
        return f'{self.user.username} профиль'
    

class CustomUser(models.Model):
    encrypted_email = models.TextField()

    @property
    def email(self):
        return decrypt_data(self.encrypted_email)

    @email.setter
    def email(self, value):
        self.encrypted_email = encrypt_data(value)
    
