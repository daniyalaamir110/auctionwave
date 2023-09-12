from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Category, Product, Bid


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class Bid(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = "__all__"


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label="Username", write_only=True)

    password = serializers.CharField(label="password", write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            if not user:
                message = "Access denied: wrong username and password"
                raise serializers.ValidationError(message, code="authorization")

        else:
            message = "Both username and password are required"
            raise serializers.ValidationError(message, code="authorization")

        attrs["user"] = user
        return attrs
