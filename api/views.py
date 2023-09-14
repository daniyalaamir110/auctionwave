from rest_framework import permissions, viewsets
from .models import Category, Product, Bid
from .serializers import (
    CategorySerializer,
    ProductReadSerializer,
    BidReadSerializer,
    ProductWriteSerializer,
    BidWriteSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProductWriteSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ProductReadSerializer
        return ProductWriteSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = BidWriteSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BidReadSerializer
        return BidWriteSerializer

    def perform_create(self, serializer):
        serializer.save(bidder=self.request.user)
