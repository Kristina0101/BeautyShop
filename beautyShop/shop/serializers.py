from rest_framework import fields, serializers
from .models import * 

class serializer_Category(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class serializer_Products(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class serializer_Brends(serializers.ModelSerializer):
    class Meta:
        model = Brends
        fields = '__all__'


class serializer_DeliveryAddress(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = '__all__'


class serializer_Payment(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class serializer_Country(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class serializer_Status(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class serializer_PaymentMethod(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

class serializer_orderDetails(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = '__all__'

class serializer_orders(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

class serializer_authUser(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = '__all__'

class serializer_roles(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'

class serializer_userRoles(serializers.ModelSerializer):
    class Meta:
        model = UserRoles
        fields = '__all__'