from rest_framework import permissions, generics, response, status
from .models import Bid
from .serializers import (
    UserBidReadSerializer,
    UserBidUpdateDeleteSerializer,
    BidWriteSerializer,
)
from common.paginations import StandardResultsSetPagination


class UserBidsListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserBidReadSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # Filter the bids which are available
        queryset = Bid.objects.filter(bidder=self.request.user).order_by("-created_at")

        return queryset


class UserBidsRetrieveView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserBidReadSerializer

    def get_queryset(self):
        # Filter the bids which are available
        queryset = Bid.objects.filter(bidder=self.request.user).order_by("-created_at")

        return queryset


class UserBidsUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserBidUpdateDeleteSerializer

    def get_queryset(self):
        # Filter the bids which are available
        queryset = Bid.objects.filter(bidder=self.request.user).order_by("-created_at")

        return queryset


class UserBidsDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserBidUpdateDeleteSerializer

    def get_queryset(self):
        # Filter the bids which are available
        queryset = Bid.objects.filter(bidder=self.request.user).order_by("-created_at")

        return queryset


class UserBidsListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserBidReadSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # Filter the bids which are available
        queryset = Bid.objects.filter(bidder=self.request.user).order_by("-created_at")

        return queryset


class BidCreateView(generics.CreateAPIView):
    serializer_class = BidWriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(bidder=self.request.user)
