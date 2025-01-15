from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'nickname', 'profile_img']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)