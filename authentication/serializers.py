# serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):   #chuyen model User sang dang JSON va nguoc lai
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'is_active')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, data):
        user = User(
            email=data['email'],
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
        )
        user.set_password(validate=data['password'])
        user.is_active = True  # Set the user to be active by default
        user.save()
        return user

#override
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token
