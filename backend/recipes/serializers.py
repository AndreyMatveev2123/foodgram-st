from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {"required": True},
            "email": {"required": True},
        }

    def validate(self, attrs):
        logger.info(f"Validating data: {attrs}")
        username = attrs.get("username")
        email = attrs.get("email")

        # Проверяем существование пользователя с таким username
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {"username": "Пользователь с таким именем уже существует"}
            )

        # Проверяем существование пользователя с таким email
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "Пользователь с таким email уже существует"}
            )

        return attrs

    def create(self, validated_data):
        logger.info(f"Creating user with data: {validated_data}")
        try:
            user = User.objects.create_user(
                username=validated_data["username"],
                email=validated_data["email"],
                password=validated_data["password"],
            )
            logger.info(f"User created successfully: {user.username}")
            return user
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise serializers.ValidationError(str(e))

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
