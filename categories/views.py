from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from .models import Category
from .serializers import CategorySerializer
from common.paginations import StandardResultsSetPagination
from common.permissions import IsAdminUserOrReadOnly
from rest_framework.parsers import FormParser, MultiPartParser

class CategoryViewSet(ModelViewSet):
    """
    A set of views to provide CRUD operations on category.
    All users can view categories, but only the super admin
    can update the categories.
    """

    queryset = Category.objects.all().order_by("title")
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdminUserOrReadOnly]
    parser_classes=[FormParser, MultiPartParser]
    filter_backends = [SearchFilter]
    search_fields = ["title"]
