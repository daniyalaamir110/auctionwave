from rest_framework import viewsets, permissions
from .models import Category
from .serializers import CategorySerializer
from common.paginations import StandardResultsSetPagination
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        # Get the ?query=& params from request
        search = self.request.query_params.get("search", None)

        # Apply filters
        if search:
            self.queryset = self.queryset.filter(title__icontains=search)

        return self.queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("search", openapi.IN_QUERY, type=openapi.TYPE_STRING)
        ],
        responses={200: CategorySerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
