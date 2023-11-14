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
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class UserBidsListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserBidReadSerializer
        elif self.request.method == "POST":
            return BidWriteSerializer
        return super().get_serializer_class()

    def get_status(self, obj):
        if obj.product.status == "ongoing":
            return "pending"

        highest_bidder = obj.product.highest_bid.bidder

        current_user = self.context["request"].user

        if highest_bidder == current_user:
            return "won"

        return "lost"

    def get_queryset(self):
        if self.request.method == "GET":
            status = self.request.query_params.get("status", None)

            queryset = (
                Bid.objects.filter(bidder=self.request.user)
                .order_by("-created_at")
                .select_related("product")
            )

            if status:
                queryset = [o for o in queryset.all() if self.get_status(o) == status]

            return queryset

        return Bid.objects.filter(bidder=self.request.user).order_by("-created_at")

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "status",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=["pending", "won", "lost"],
            ),
        ],
        responses={200: UserBidReadSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(bidder=self.request.user)


class UserBidsDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsBidder]

    def get_queryset(self):
        if self.request.method == "GET":
            return Bid.objects.all().order_by("-created_at").select_related("product")
        else:
            return Bid.objects.all().order_by("-created_at")

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
