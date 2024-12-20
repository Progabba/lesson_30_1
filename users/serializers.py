from rest_framework import serializers
from .models import Payment, CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#
#         # Добавление пользовательских полей в токен
#         token['username'] = user.username
#         token['email'] = user.email
#
#         return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
