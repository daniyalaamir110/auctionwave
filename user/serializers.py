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
    This serializer allows editing a user
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
            "email",
            "first_name",
            "last_name",
            "current_password",
            "new_password",
            "confirm_password",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def update(self, instance, validated_data):
        current_password = validated_data.get("current_password", None)
        new_password = validated_data.get("new_password", None)

        if current_password and not self.request.user.check_password(current_password):
            raise serializers.ValidationError(
                {"current_password": "Incorrect password."}
            )

        if new_password:
            self.request.user.set_password(new_password)

        self.request.user.first_name = validated_data.get(
            "first_name", self.request.user.first_name
        )
        self.request.user.last_name = validated_data.get(
            "last_name", self.request.user.last_name
        )
        self.request.user.email = validated_data.get("email", self.request.user.email)
        self.request.user.save()

        return self.request.user


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
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "password2",
            "email",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
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
