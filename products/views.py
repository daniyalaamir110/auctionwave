from rest_framework import permissions, generics, exceptions, response, status
from .models import Product
from .serializers import ProductReadSerializer, ProductWriteSerializer
from datetime import datetime, timezone


class ProductRetrieveView(generics.RetrieveAPIView):
    serializer_class = ProductReadSerializer

    # Only includes the available products
    queryset = Product.objects.filter(valid_till__gte=datetime.now(tz=timezone.utc))


class ProductListView(generics.ListAPIView):
    serializer_class = ProductReadSerializer

    def get_queryset(self):
        # Filter the products which are available
        queryset = Product.objects.filter(valid_till__gte=datetime.now(tz=timezone.utc))

        # Get the ?query params from request
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


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductWriteSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


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
