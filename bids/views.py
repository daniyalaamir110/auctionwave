from rest_framework import permissions, generics
from .models import Bid
from .serializers import UserBidReadSerializer
from common.paginations import StandardResultsSetPagination


class UserBidsListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserBidReadSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # Filter the bids which are available
        queryset = Bid.objects.filter(bidder=self.request.user).order_by("-created_at")

        return queryset
