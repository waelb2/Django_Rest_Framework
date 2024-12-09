from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from users.models import Buyer, Saleman, User, UserRole


class RegisterUserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(UserRole.choices(), required=True)
    store_name = serializers.CharField(required=False)
    budget = serializers.DecimalField(decimal_places=2, max_digits=10, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "role",
            "email",
            "password",
            "budget",
            "store_name",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        # Check if email already exists in the database
        if User.objects.filter(email=value).exists():
            raise DjangoValidationError("A user with this email already exists.")
        return value

    def validate(self, data):
        # validate fields based on roles
        user_role = data.get("role")
        if user_role == UserRole.SALEMAN.value:
            if not data.get("store_name"):
                raise serializers.ValidationError(
                    {"sotre_name": "store name is required for a saleman"}
                )
        else:
            if not data.get("budget"):
                raise serializers.ValidationError(
                    {"budget": "budget is required for a buyer"}
                )

        # Validate the password
        password = data.get("password")
        user_data = {
            key: data[key]
            for key in ["username", "first_name", "last_name"]
            if key in data
        }
        user = User(**user_data)
        try:
            validate_password(password=password, user=user)
        except DjangoValidationError as err:
            raise serializers.ValidationError({"password": err.messages})
        return super().validate(data)

    def create(self, validated_data):
        user_fields = {
            "username": validated_data.pop("username"),
            "first_name": validated_data.pop("first_name"),
            "last_name": validated_data.pop("last_name"),
            "email": validated_data.pop("email"),
            "password": validated_data.pop("password"),
            "role": validated_data.pop("role"),
        }
        user = User.objects.create_user(**user_fields)
        if user.role == UserRole.SALEMAN.value:
            store_name = validated_data.get("store_name")
            saleman = Saleman.objects.create(user=user, store_name=store_name)
        else:
            budget = validated_data.get("budget")
            buyer = Buyer.objects.create(user=user, budget=budget)
        return user
