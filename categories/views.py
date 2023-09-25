from rest_framework import viewsets, filters
from .models import Category
from .serializers import CategorySerializer
from common.paginations import StandardResultsSetPagination
from common.permissions import IsAdminUserOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A set of views to provide CRUD operations on category.
    All users can view categories, but only the super admin
    can update the categories.
    """

    queryset = Category.objects.all().order_by("title")
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]
