from user.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import (
    EmailField,
    CharField,
    ModelSerializer,
    Serializer,
    BooleanField,
    ImageField
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

    is_self = BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "is_self",
            "profile_image"
        ]

        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "profile_image": {"required": True}
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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            data["is_self"] = instance == request.user
        return data


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


class ProfileImageUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('profile_image',)