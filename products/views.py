from rest_framework import permissions, generics, filters
from .models import Product
from .serializers import (
    ProductReadSerializer,
    ProductWriteSerializer,
    ProductBidsReadSerializer,
)
from datetime import datetime, timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from common.paginations import StandardResultsSetPagination
from common.permissions import IsProductCreator


class ProductRetrieveView(generics.RetrieveAPIView):
    """
    This resource returns the details of a valid product
    """

    serializer_class = ProductReadSerializer

    # Only includes the available products
    queryset = Product.objects.filter(valid_till__gte=datetime.now(tz=timezone.utc))


class ProductListView(generics.ListAPIView):
    """
    This resource returns paginated, filtered, and ordered
    list of products as needed which are valid.
    """

    serializer_class = ProductReadSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        # Filter the products which are available
        queryset = Product.objects.filter(
            valid_till__gte=datetime.now(tz=timezone.utc)
        ).order_by("-created_at")

        # Get the ?query=& params from request
        category_id = self.request.query_params.get("category", None)
        min_price = self.request.query_params.get("min_price", None)
        max_price = self.request.query_params.get("max_price", None)
        creator_id = self.request.query_params.get("creator", None)

        # Apply filters
        if creator_id:
            queryset = queryset.filter(creator_id=creator_id)

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if min_price:
            queryset = queryset.filter(base_price__gte=min_price)

        if max_price:
            queryset = queryset.filter(base_price__lte=max_price)

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("category", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("creator", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("min_price", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("max_price", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={200: ProductReadSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CurrentUserProductListView(generics.ListAPIView):
    """
    This resource returns the products created by the current user.
    Must be logged in to access.
    """

    serializer_class = ProductReadSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        queryset = Product.objects.filter(creator_id=self.request.user.pk).order_by(
            "-created_at"
        )

        # Get the ?query=& params from request
        search = self.request.query_params.get("search", None)
        category_id = self.request.query_params.get("category", None)
        min_price = self.request.query_params.get("min_price", None)
        max_price = self.request.query_params.get("max_price", None)

        # Apply filters
        if search:
            queryset = queryset.filter(title__icontains=search)

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if min_price:
            queryset = queryset.filter(base_price__gte=min_price)

        if max_price:
            queryset = queryset.filter(base_price__lte=max_price)

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("category", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("min_price", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("max_price", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={200: ProductReadSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CurrentUserProductRetrieveView(generics.RetrieveAPIView):
    """
    This resource returns a single product created by the current user.
    Must be logged in to access.
    """

    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductReadSerializer
    permission_classes = [permissions.IsAuthenticated, IsProductCreator]


class ProductCreateView(generics.CreateAPIView):
    """
    This resource lets create a product with a base amount and max validity time
    """

    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductWriteSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class ProductDeleteView(generics.DestroyAPIView):
    """
    This resource lets delete a product out of the owned products.
    """

    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductWriteSerializer
    permission_classes = [permissions.IsAuthenticated, IsProductCreator]


class ProductBidsListView(generics.RetrieveAPIView):
    """
    This resource returns the list of bids for a specific product
    which is valid
    """

    serializer_class = ProductBidsReadSerializer
    queryset = Product.objects.filter(valid_till__gte=datetime.now(tz=timezone.utc))


class UserProductBidsListView(generics.RetrieveAPIView):
    """
    This resource returns the list of bids for a specific product
    created by the current user
    """

    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductBidsReadSerializer
    permission_classes = [permissions.IsAuthenticated, IsProductCreator]
