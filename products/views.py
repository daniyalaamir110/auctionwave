from rest_framework import permissions, generics, exceptions, response, status
from .models import Product
from .serializers import ProductReadSerializer, ProductWriteSerializer
from datetime import datetime, timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class ProductRetrieveView(generics.RetrieveAPIView):
    serializer_class = ProductReadSerializer

    # Only includes the available products
    queryset = Product.objects.filter(valid_till__gte=datetime.now(tz=timezone.utc))


class ProductListView(generics.ListAPIView):
    serializer_class = ProductReadSerializer

    PAGE_SIZE = 20

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
        page = self.request.query_params.get("page", None)

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

        if not page:
            page = 0
        else:
            page = int(page)

        return queryset[page * self.PAGE_SIZE : (page + 1) * self.PAGE_SIZE]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("category", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("creator", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("search", openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter("min_price", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("max_price", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("page", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={200: ProductReadSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CurrentUserProductListView(generics.ListAPIView):
    serializer_class = ProductReadSerializer
    permission_classes = [permissions.IsAuthenticated]
    PAGE_SIZE = 20

    def get_queryset(self):
        queryset = Product.objects.filter(creator_id=self.request.user.pk).order_by(
            "-created_at"
        )

        # Get the ?query=& params from request
        search = self.request.query_params.get("search", None)
        category_id = self.request.query_params.get("category", None)
        min_price = self.request.query_params.get("min_price", None)
        max_price = self.request.query_params.get("max_price", None)
        page = self.request.query_params.get("page", None)

        # Apply filters
        if search:
            queryset = queryset.filter(title__icontains=search)

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if min_price:
            queryset = queryset.filter(base_price__gte=min_price)

        if max_price:
            queryset = queryset.filter(base_price__lte=max_price)

        if not page:
            page = 0
        else:
            page = int(page)

        return queryset[page * self.PAGE_SIZE : (page + 1) * self.PAGE_SIZE]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("category", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("search", openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter("min_price", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("max_price", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("page", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
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
        return super().get_queryset()


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductWriteSerializer

    def delete(self, request, *args, **kwargs):
        # Get the product by its ID
        product = self.get_object()

        if not product:
            raise exceptions.NotFound("Product doesn't exist")

        # Check if the user is the creator of the product
        if request.user != product.creator:
            raise exceptions.PermissionDenied(
                "You do not have permission to delete this product."
            )

        # Delete the product
        product.delete()

        return response.Response(status=status.HTTP_204_NO_CONTENT)
