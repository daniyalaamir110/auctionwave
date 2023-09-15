from rest_framework import permissions, viewsets, generics
from .models import Bid
from .serializers import BidReadSerializer, UserBidReadSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class UserBidsListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserBidReadSerializer
    PAGE_SIZE = 20

    def get_queryset(self):
        # Filter the bids which are available
        queryset = Bid.objects.filter(bidder=self.request.user).order_by("-created_at")

        # Get the ?query=& params from request
        page = self.request.query_params.get("page", None)

        # Apply pagination
        if not page:
            page = 0
        else:
            page = int(page)

        return queryset[page * self.PAGE_SIZE : (page + 1) * self.PAGE_SIZE]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("page", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={200: UserBidReadSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
