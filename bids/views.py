from rest_framework import permissions, viewsets
from .models import Bid
from .serializers import BidReadSerializer, BidWriteSerializer


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
