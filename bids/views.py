from rest_framework import permissions, generics
from .models import Bid
from .serializers import (
    UserBidReadSerializer,
    UserBidUpdateDeleteSerializer,
    BidWriteSerializer,
)
from common.paginations import StandardResultsSetPagination
from common.permissions import IsBidder, IsBidProductValid


class UserBidsListView(generics.ListAPIView):
    """
    This resource returns a list of bids the currently
    logged in user has made. User must be logged in to
    access this resource.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserBidReadSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Bid.objects.filter(bidder=self.request.user).order_by("-created_at")

        return queryset


class UserBidsRetrieveView(generics.RetrieveAPIView):
    """
    This resource returns the bids done by the current user
    on others' products.
    """

    queryset = Bid.objects.all().order_by("-created_at")
    permission_classes = [permissions.IsAuthenticated, IsBidder]
    serializer_class = UserBidReadSerializer


class UserBidsUpdateView(generics.UpdateAPIView):
    """
    This resource lets update the bid amount of an existing bid
    if the product is valid.
    """

    queryset = Bid.objects.all().order_by("-created_at")
    permission_classes = [permissions.IsAuthenticated, IsBidder, IsBidProductValid]
    serializer_class = UserBidUpdateDeleteSerializer


class UserBidsDeleteView(generics.DestroyAPIView):
    """
    This resource lets cancel an existing bid done by the user,
    if the product is available.
    """

    queryset = Bid.objects.all().order_by("-created_at")
    permission_classes = [permissions.IsAuthenticated, IsBidder, IsBidProductValid]


class BidCreateView(generics.CreateAPIView):
    """
    This resource lets a user create a bid on a product, created by other
    users that is available.
    """

    serializer_class = BidWriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(bidder=self.request.user)
