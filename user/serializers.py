from rest_framework import serializers, validators
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class UserReadSerializer(serializers.ModelSerializer):
    """
    This serializer contains the user basic info only
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        ]


class UserEditSerailizer(serializers.ModelSerializer):
    """
    This serializer allows editing a user.
    """

    current_password = serializers.CharField(
        write_only=True, required=True, max_length=128
    )
    new_password = serializers.CharField(
        write_only=True, required=False, max_length=128, allow_blank=True
    )
    confirm_password = serializers.CharField(
        write_only=True, required=False, max_length=128, allow_blank=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "current_password",
            "new_password",
            "confirm_password",
        ]
        extra_kwargs = {
            "email": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "current_password": {"required": True},
            "new_password": {"required": False},
            "confirm_password": {"required": False},
        }

    def create(self, validated_data):
        current_password = validated_data.get("current_password", None)
        new_password = validated_data.get("new_password", None)
        confirm_password = validated_data.get("confirm_password", None)
        user = validated_data.get("user", None)

        if current_password and not user.check_password(current_password):
            raise serializers.ValidationError(
                {"current_password": "Incorrect password."}
            )

        if new_password:
            if new_password == confirm_password:
                user.set_password(new_password)
            else:
                raise serializers.ValidationError(
                    {"confirm_password": "Password fields don't match."}
                )

        user.first_name = validated_data.get("first_name", user.first_name)
        user.last_name = validated_data.get("last_name", user.last_name)
        user.email = validated_data.get("email", user.email)
        user.save()

        return user


class RegisterSerializer(serializers.ModelSerializer):
    """
    This serializer allows creation of new user
    """

    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "confirm_password",
            "email",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

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
