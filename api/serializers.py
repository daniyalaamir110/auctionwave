from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Product, Bid


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class BidReadSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer(read_only=True)
    bidder = UserSerializer(read_only=True)

    class Meta:
        model = Bid
        fields = "__all__"


class BidWriteSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer(read_only=True)
    bidder = UserSerializer(read_only=True)

    class Meta:
        model = Bid
        fields = "__all__"
        read_only_fields = ["bidder"]
