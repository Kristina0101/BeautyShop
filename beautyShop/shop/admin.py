from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Brends)
admin.site.register(Category)
admin.site.register(DeliveryAddress)
admin.site.register(OrderDetails)
admin.site.register(Orders)
admin.site.register(Payment)
admin.site.register(Products)
admin.site.register(Roles)
admin.site.register(UserRoles)
admin.site.register(Country)
admin.site.register(AuthUser)
admin.site.register(PaymentMethod)
admin.site.register(Status)