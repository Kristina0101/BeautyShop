# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=100)

    def __str__(self):
        return self.country_name
    class Meta:
        managed = False
        db_table = 'country'

# у человека сильно сейчас играет юнешеский маскимализм  
class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    name_status = models.CharField(max_length=100)

    def __str__(self):
        return self.name_status
    class Meta:
        managed = False
        db_table = 'status'

class PaymentMethod(models.Model):
    payment_method_id = models.AutoField(primary_key=True)
    payment_method = models.CharField(max_length=200)

    def __str__(self):
        return self.payment_method
    class Meta:
        managed = False
        db_table = 'payment_method'

class Brends(models.Model):
    brend_id = models.AutoField(primary_key=True)
    name_brand = models.CharField(max_length=100)
    country = models.ForeignKey('Country', models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.name_brand
    class Meta:
        managed = False
        db_table = 'brends'


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name_category = models.CharField(max_length=100)

    def __str__(self):
            return self.name_category
    class Meta:
        managed = False
        db_table = 'category'


class DeliveryAddress(models.Model):
    delivery_address_id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING, blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)

    def __str__(self):
        return self.order.user.username
    class Meta:
        managed = False
        db_table = 'delivery_address'


class OrderDetails(models.Model):
    order_details_id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING, blank=True, null=True)
    products = models.ForeignKey('Products', models.DO_NOTHING, blank=True, null=True)
    quantity_products = models.IntegerField()
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.ForeignKey('Status', models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.order.user.username
    class Meta:
        managed = False
        db_table = 'order_details'


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dates_order = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.user.username
    class Meta:
        managed = False
        db_table = 'orders'


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, models.DO_NOTHING, blank=True, null=True)
    date_payment = models.DateTimeField()
    sum_payment = models.DecimalField(max_digits=15, decimal_places=2)
    payment_method = models.ForeignKey('PaymentMethod', models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.order.user.username
    class Meta:
        managed = False
        db_table = 'payment'


class Products(models.Model):
    products_id = models.AutoField(primary_key=True)
    photo_product = models.ImageField(upload_to='products/%Y/%m/%d')
    name_product = models.CharField(max_length=100)
    brend = models.ForeignKey(Brends, models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name_product
    class Meta:
        managed = False
        db_table = 'products'

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
            return self.username
    class Meta:
        managed = False
        db_table = 'auth_user'

class Roles(models.Model):
    roles_id = models.AutoField(primary_key=True)
    name_role = models.CharField(max_length=50)

    def __str__(self):
        return self.name_role
    class Meta:
        managed = False
        db_table = 'roles'


class UserRoles(models.Model):
    roles = models.ForeignKey(Roles, models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_roles_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.user.username
    class Meta:
        managed = False
        db_table = 'user_roles'


