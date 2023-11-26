from rest_framework import serializers
from categories.serializers import CategorySerializer
from user.serializers import UserSerializer
from .models import Product
from django.core.exceptions import ValidationError
from datetime import datetime, timezone
from bids.models import Bid


class ProductBidReadSerializer(serializers.ModelSerializer):
    bidder = UserSerializer(read_only=True)
    rank = serializers.IntegerField(read_only=True)

    class Meta:
        model = Bid
        exclude = ["product"]


class ProductBidsReadSerializer(serializers.ModelSerializer):
    bidder = UserSerializer(read_only=True)
    rank = serializers.IntegerField(read_only=True)

    class Meta:
        model = Bid
        exclude = ["product"]


class ProductReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    creator = UserSerializer(read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    time_left = serializers.CharField(read_only=True)
    highest_bid = ProductBidReadSerializer(read_only=True)
    current_user_bid = serializers.SerializerMethodField(read_only=True)
    bid_count = serializers.IntegerField(read_only=True)
    is_creator = serializers.SerializerMethodField()
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "image",
            "base_price",
            "valid_till",
            "is_sold",
            "status",
            "category",
            "creator",
            "is_available",
            "time_left",
            "highest_bid",
            "current_user_bid",
            "bid_count",
            "is_creator",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "highest_bid": {"read_only": True},
        }

    def get_current_user_bid(self, obj):
        current_user = self.context["request"].user

        if current_user.id:
            try:
                current_user_bid = obj.bids.get(bidder=current_user)
                return ProductBidReadSerializer(current_user_bid).data
            except Bid.DoesNotExist:
                return None

        else:
            return None

    def get_is_creator(self, obj):
        current_user = self.context["request"].user

        is_creator = obj.creator.id == current_user.id

        return is_creator


class ProductWriteSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)

    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "category",
            "base_price",
            "valid_till",
            "image",
        ]

    def validate(self, attrs):
        if attrs["valid_till"] < datetime.now(tz=timezone.utc):
            raise ValidationError(
                {"valid_till": "Must be not be less than the current time"}
            )

        if attrs["base_price"] <= 0:
            raise ValidationError({"base_price": "Must be a positive integer"})

        return attrs
