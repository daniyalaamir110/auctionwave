from rest_framework import serializers
from .models import Bid
from products.serializers import ProductReadSerializer
from user.serializers import UserReadSerializer


class BidReadSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer(read_only=True)
    bidder = UserReadSerializer(read_only=True)

    class Meta:
        model = Bid
        fields = "__all__"


class BidWriteSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer(read_only=True)
    bidder = UserReadSerializer(read_only=True)

    class Meta:
        model = Bid
        fields = "__all__"
        read_only_fields = ["bidder"]
