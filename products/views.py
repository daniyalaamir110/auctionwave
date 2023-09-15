from rest_framework import permissions, generics, exceptions, response, status
from .models import Product
from .serializers import ProductReadSerializer, ProductWriteSerializer
from datetime import datetime, timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from bids.models import Bid
from bids.serializers import BidWriteSerializer


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

    def create(self, request, product_id, *args, **kwargs):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return response.Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if product.creator.pk == self.request.user.pk:
            return response.Response(
                {"error": "You cannot bid on your own product"},
                status=status.HTTP_403_FORBIDDEN,
            )

        bid_amount = request.data.get("bid_amount")

        if not bid_amount:
            return response.Response(
                {"error": "bid_amount is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            bid_amount = int(bid_amount)
        except ValueError:
            return response.Response(
                {"error": "bid_amount must be a positive integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if bid_amount <= product.base_price:
            return response.Response(
                {"error": "Bid amount must be higher than the base price"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Bid.objects.filter(product=product, bidder=request.user).count():
            return response.Response(
                {"error": "This user has already bid for this product"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create the Bid object
        bid = Bid.objects.create(
            product=product, bidder=request.user, bid_amount=bid_amount
        )

        serializer = BidWriteSerializer(bid)

        return response.Response(serializer.data, status=status.HTTP_201_CREATED)
