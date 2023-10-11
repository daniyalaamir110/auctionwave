from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import (
    EmailField,
    CharField,
    ModelSerializer,
    Serializer,
)
from rest_framework.validators import UniqueValidator


class UserSerializer(ModelSerializer):
    """
    This serializer contains the user basic info only
    """

    email = EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    password = CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
        ]

        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class UserUpdatePasswordSerializer(ModelSerializer):
    """
    This serializer allows to update the password of a user
    """

    password = CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = ["password"]


class UsernameSuggestionSerializer(Serializer):
    first_name = CharField(required=True)
    last_name = CharField(required=True)


class UsernameAvailabilitySerializer(Serializer):
    username = CharField(required=True)


class EmailAvailabilitySerializer(Serializer):
    email = EmailField(required=True)
