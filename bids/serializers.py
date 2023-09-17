from rest_framework import serializers
from .models import Bid
from products.models import Product
from products.serializers import ProductReadSerializer
from user.serializers import UserReadSerializer


class BidReadSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer(read_only=True)
    bidder = UserReadSerializer(read_only=True)

    class Meta:
        model = Bid
        fields = "__all__"


class UserBidReadSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer(read_only=True)

    class Meta:
        model = Bid
        exclude = ["bidder"]


class ProductBidReadSerializer(serializers.ModelSerializer):
    bidder = UserReadSerializer(read_only=True)

    class Meta:
        model = Bid
        fields = "__all__"


class BidWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = "__all__"
        read_only_fields = ["bidder", "product"]

    def validate(self, attrs):
        product_id = self.context.get("product_id")
        request = self.context.get("request")
        bid_amount = attrs.get("bid_amount")

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"error": "Product not found"})

        if product.creator == request.user:
            raise serializers.ValidationError(
                {"error": "You cannot bid on your own product"}
            )

        if not bid_amount:
            raise serializers.ValidationError({"error": "bid_amount is required"})

        try:
            bid_amount = int(bid_amount)
        except ValueError:
            raise serializers.ValidationError(
                {"error": "bid_amount must be a positive integer"}
            )

        if bid_amount <= product.base_price:
            raise serializers.ValidationError(
                {"error": "Bid amount must be higher than the base price"}
            )

        if Bid.objects.filter(product=product, bidder=request.user).exists():
            raise serializers.ValidationError(
                {"error": "This user has already bid for this product"}
            )

        return attrs
