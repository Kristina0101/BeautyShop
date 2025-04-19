from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
class CustomUserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.email = obj.email
        super().save_model(request, obj, form, change)

admin.site.register(CustomUser, CustomUserAdmin)