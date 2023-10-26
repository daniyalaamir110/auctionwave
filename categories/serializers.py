from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer handling the CRUD of category
    """

    image = serializers.ImageField(required=True)

    class Meta:
        model = Category
        fields = ["id", "title", "image", "created_at", "updated_at"]
        
