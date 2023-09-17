from rest_framework import permissions, generics, exceptions, response, status, filters
from .models import Product
from .serializers import ProductReadSerializer, ProductWriteSerializer
from datetime import datetime, timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from bids.models import Bid
from bids.serializers import BidWriteSerializer
from common.paginations import StandardResultsSetPagination


class ProductRetrieveView(generics.RetrieveAPIView):
    serializer_class = ProductReadSerializer

    # Only includes the available products
    queryset = Product.objects.filter(valid_till__gte=datetime.now(tz=timezone.utc))


class ProductListView(generics.ListAPIView):
    serializer_class = ProductReadSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        # Filter the products which are available
        queryset = Product.objects.filter(
            valid_till__gte=datetime.now(tz=timezone.utc)
        ).order_by("-created_at")

        # Get the ?query=& params from request
        search = self.request.query_params.get("search", None)
        category_id = self.request.query_params.get("category", None)
        min_price = self.request.query_params.get("min_price", None)
        max_price = self.request.query_params.get("max_price", None)
        creator_id = self.request.query_params.get("creator", None)

        # Apply filters
        if creator_id:
            queryset = queryset.filter(creator_id=creator_id)

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
            openapi.Parameter("creator", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("search", openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter("min_price", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("max_price", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={200: ProductReadSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CurrentUserProductListView(generics.ListAPIView):
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
            # openapi.Parameter("search", openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter("min_price", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("max_price", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={200: ProductReadSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CurrentUserProductRetrieveView(generics.RetrieveAPIView):
    serializer_class = ProductReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Product.objects.filter(creator_id=self.request.user.pk).order_by(
            "-created_at"
        )

        return queryset

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ProductCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductWriteSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(creator_id=self.request.user.pk).order_by(
            "-created_at"
        )

        return queryset


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductWriteSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(creator_id=self.request.user.pk).order_by(
            "-created_at"
        )

        return queryset

    def delete(self, request, *args, **kwargs):
        # Get the product by its ID
        product = self.get_object()

        if not product:
            raise exceptions.NotFound("Product not found")

        # Delete the product
        product.delete()

        return response.Response(status=status.HTTP_204_NO_CONTENT)


class ProductBidCreateView(generics.CreateAPIView):
    serializer_class = BidWriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, id):
        serializer = self.get_serializer(
            data=request.data, context={"product_id": id, "request": request}
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return response.Response(serializer.data, status=status.HTTP_201_CREATED)
