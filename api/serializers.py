from rest_framework import serializers
from .models import Category, Product, Bid

class ModelSerializerWithUser(serializers.ModelSerializer):

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = "__all__"