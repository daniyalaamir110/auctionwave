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
from common.permissions import IsProductCreator, IsProductAuctionEnded, IsProductNotSold
from bids.models import Bid
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.db.models.query import Q


class ProductDetailView(RetrieveDestroyAPIView):
    serializer_class = ProductReadSerializer

    queryset = Product.objects.filter(
        valid_till__gte=datetime.now(tz=timezone.utc)
    ).select_related("category", "creator")

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsProductCreator()]
        return super().get_permissions()
    


class ProductListView(ListCreateAPIView):
    serializer_class = ProductReadSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title"]
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductReadSerializer
        elif self.request.method == "POST":
            return ProductWriteSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        if self.request.method == "GET":
            # Filter the products which are available
            queryset = (
                Product.objects.filter(valid_till__gte=datetime.now(tz=timezone.utc))
                .order_by("-created_at")
                .select_related("category", "creator")
            )

            # Get the ?query=& params from request
            category_id = self.request.query_params.get("category", None)
            min_price = self.request.query_params.get("min_price", None)
            max_price = self.request.query_params.get("max_price", None)
            creator_id = self.request.query_params.get("creator", None)
            exclude = self.request.query_params.get("exclude", None)
            status = self.request.query_params.get("status", None)

            # Apply filters
            if creator_id:
                queryset = queryset.filter(creator_id=creator_id)

            if category_id:
                queryset = queryset.filter(category_id=category_id)

            if exclude:
                queryset = queryset.filter(~Q(id=exclude))

            if min_price:
                queryset = queryset.filter(base_price__gte=min_price)

            if max_price:
                queryset = queryset.filter(base_price__lte=max_price)

            if status:
                ids = [o.id for o in queryset.all() if o.status == status]
                queryset = queryset.filter(pk__in=ids)

            return queryset

        elif self.request.method == "POST":
            return Product.objects.all()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("category", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("exclude", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("creator", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("min_price", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("max_price", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                "status",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=["ongoing", "finished", "sold"],
            ),
        ],
        responses={200: ProductReadSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CurrentUserProductListView(ListAPIView):
    """
    This resource returns the products created by the current user.
    Must be logged in to access.
    """

    serializer_class = ProductReadSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title"]
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = (
            Product.objects.filter(
                creator_id=self.request.user.pk,
            )
            .order_by("-created_at")
            .select_related("category")
        )

        # Get the ?query=& params from request
        category_id = self.request.query_params.get("category", None)
        min_price = self.request.query_params.get("min_price", None)
        max_price = self.request.query_params.get("max_price", None)
        status = self.request.query_params.get("status", None)

        # Apply filters
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if min_price:
            queryset = queryset.filter(base_price__gte=min_price)

        if max_price:
            queryset = queryset.filter(base_price__lte=max_price)

        if status:
            ids = [o.id for o in queryset.all() if o.status == status]
            queryset = queryset.filter(pk__in=ids)

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("category", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("min_price", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("max_price", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                "status",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=["ongoing", "finished", "sold"],
            ),
        ],
        responses={200: ProductReadSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CurrentUserProductRetrieveView(RetrieveAPIView):
    """
    This resource returns a single product created by the current user.
    Must be logged in to access.
    """

    queryset = Product.objects.all().order_by("-created_at").select_related("category")
    serializer_class = ProductReadSerializer
    permission_classes = [IsAuthenticated, IsProductCreator]


class ProductBidsListView(ListAPIView):
    """
    This resource returns the top 5 list of bids for a specific product
    which is valid.
    """

    serializer_class = ProductBidsReadSerializer

    def get_queryset(self):
        return (
            Bid.objects.filter(product__id=self.kwargs["pk"])
            .order_by("-bid_amount", "updated_at")
            .select_related("bidder")[:5]
        )


class UserProductBidsListView(ListAPIView):
    """
    This resource returns the list of bids for a specific product
    created by the current user
    """

    serializer_class = ProductBidsReadSerializer
    permission_classes = [IsAuthenticated, IsProductCreator]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return (
            Bid.objects.filter(
                product__id=self.kwargs["pk"],
                product__creator__id=self.request.user.id,
            )
            .order_by("-bid_amount")
            .select_related("bidder")
        )


class ProductSellView(UpdateAPIView):
    """
    This resource marks an item as sold
    """

    queryset = Product.objects.all()
    permission_classes = [
        IsAuthenticated,
        IsProductCreator,
        IsProductAuctionEnded,
        IsProductNotSold,
    ]
    lookup_field = "id"

    def update(self):
        instance = self.get_object()
        instance.sold = True
        instance.save()
        return Response({"detail": "Product marked as sold"}, status=HTTP_200_OK)
