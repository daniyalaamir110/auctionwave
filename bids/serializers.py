from rest_framework import serializers, fields
from .models import Bid
from products.models import Product
from products.serializers import ProductReadSerializer
from user.serializers import UserReadSerializer
from datetime import datetime, timezone


class BidReadSerializer(serializers.ModelSerializer):
    """
    Serializer with bid info, along with bidder and product.
    """

    product = ProductReadSerializer(read_only=True)
    bidder = UserReadSerializer(read_only=True)

    class Meta:
        model = Bid
        fields = "__all__"


class UserBidReadSerializer(serializers.ModelSerializer):
    """
    Serializer with bid info of a user, along with product.
    """

    product = ProductReadSerializer(read_only=True)

    class Meta:
        model = Bid
        exclude = ["bidder"]


class UserBidUpdateDeleteSerializer(serializers.ModelSerializer):
    """
    Serializer with bid info of a product, along with bidder.
    """

    class Meta:
        model = Bid
        fields = ["bid_amount"]


class BidWriteSerializer(serializers.ModelSerializer):
    """
    Serializer that handles bid creation, updation, delete.
    """

    product_id = fields.IntegerField(write_only=True)

    class Meta:
        model = Bid
        fields = "__all__"
        read_only_fields = ["bidder", "product"]

    def validate(self, attrs):
        product_id = attrs.get("product_id")
        request = self.context.get("request")
        bid_amount = attrs.get("bid_amount")

        # Get the product object
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"error": "Product not found"})

        # Check if the product is valid
        if product.valid_till < datetime.now(tz=timezone.utc):
            raise serializers.ValidationError({"error": "Product has been sold"})

        # Check if the current user is not the actual creator of product
        if product.creator == request.user:
            raise serializers.ValidationError(
                {"error": "You cannot bid on your own product"}
            )

        # Check if bid amount was provided
        if not bid_amount:
            raise serializers.ValidationError({"error": "bid_amount is required"})

        # Check if bid amount is a valid integer
        try:
            bid_amount = int(bid_amount)
        except ValueError:
            raise serializers.ValidationError(
                {"error": "bid_amount must be a positive integer"}
            )

        # Check if bid amount is not less than the base price
        if bid_amount < product.base_price:
            raise serializers.ValidationError(
                {"error": "Bid amount must be higher than the base price"}
            )

        # Check if there is no existing bid done by the user on the same product
        if Bid.objects.filter(product=product, bidder=request.user).exists():
            raise serializers.ValidationError(
                {"error": "This user has already bid for this product"}
            )

        return attrs
