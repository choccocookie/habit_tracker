from rest_framework import serializers
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'phone', 'сity', 'avatar', 'telegram_chat_id')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone'),
            сity=validated_data.get('сity'),
            avatar=validated_data.get('avatar'),
            telegram_chat_id=validated_data.get('telegram_chat_id'),
        )
        return user
