from rest_framework import serializers
from categories.serializers import CategorySerializer
from user.serializers import UserReadSerializer
from .models import Product
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta, timezone


class ProductReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    creator = UserReadSerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "category",
            "base_price",
            "valid_till",
        ]

    def validate(self, attrs):
        if attrs["valid_till"] < datetime.now(tz=timezone.utc):
            raise ValidationError(
                {"valid_till": "Must be not be less than the current time"}
            )

        if attrs["base_price"] <= 0:
            raise ValidationError({"base_price": "Must be a positive integer"})

        return attrs
