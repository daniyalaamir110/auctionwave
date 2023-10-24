from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from .models import Bid
from .serializers import (
    UserBidReadSerializer,
    UserBidUpdateSerializer,
    BidWriteSerializer,
)
from common.paginations import StandardResultsSetPagination
from common.permissions import IsBidder, IsBidProductValid


class UserBidsListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserBidReadSerializer
        elif self.request.method == "POST":
            return BidWriteSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if self.request.method == "GET":
            return (
                Bid.objects.filter(bidder=self.request.user)
                .order_by("-created_at")
                .select_related("product")
            )
        return Bid.objects.filter(bidder=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(bidder=self.request.user)


class UserBidsDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsBidder]

    def get_queryset(self):
        if self.request.method == "GET":
            return Bid.objects.all().order_by("-created_at").select_related("product")
        else:
            return Bid.objects.all().order_by("-created_at")
        # return super().get_queryset()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserBidReadSerializer
        elif self.request.method in ("POST", "PUT", "PATCH"):
            return UserBidUpdateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated, IsBidder]
        if self.request.method not in SAFE_METHODS:
            self.permission_classes.append(IsBidProductValid)
        return super().get_permissions()
