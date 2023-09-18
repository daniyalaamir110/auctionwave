from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer handling the CRUD of category
    """

    class Meta:
        model = Category
        fields = "__all__"
