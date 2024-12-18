from django import forms
from .models import *


class BrendsForm(forms.ModelForm):
    class Meta:
        model = Brends
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'


class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = '__all__'


class OrderDetailsForm(forms.ModelForm):
    class Meta:
        model = OrderDetails
        fields = '__all__'
        labels = {
            'order': 'Заказ',
            'products': 'Продукты',
            'quantity_products': 'Количество продуктов',
            'unit_price': 'Цена за единицу',
            'status': 'Статус',
        }


class OrdersForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = '__all__'


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'


class RolesForm(forms.ModelForm):
    class Meta:
        model = Roles
        fields = '__all__'


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = '__all__'


class UserRolesForm(forms.ModelForm):
    class Meta:
        model = UserRoles
        fields = '__all__'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class OrderForm(forms.Form):
    address = forms.CharField(label="Адрес доставки", max_length=255)
    city = forms.CharField(label="Город", max_length=100)
    postcode = forms.CharField(label="Почтовый индекс", max_length=20)
    payment_method = forms.ChoiceField(label="Способ оплаты", choices=[("card", "Карта"), ("cash", "Наличные")])