from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from products.models import Product
from bids.models import Bid
from datetime import datetime, timezone
from django.db.models import F, Count, ExpressionWrapper, DecimalField
from products.serializers import ProductReadSerializer
from bids.serializers import UserBidReadSerializer


class DashboardRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    @action(methods=["GET"], detail=False)
    def retrieve(self, request):
        user = request.user

        # Ongoing auctions
        ongoing_auctions = self.get_ongoing_auctions(user=user)
        top_ongoing_auctions = ProductReadSerializer(
            ongoing_auctions[:5], many=True, context={"request": request}
        ).data
        ongoing_auctions_count = ongoing_auctions.count()

        # Completed auctions
        completed_auctions = self.get_completed_auctions(user=user)
        completed_auctions_count = completed_auctions.count()

        # Pending bids
        pending_bids = self.get_pending_bids(user=user)
        top_pending_bids = UserBidReadSerializer(
            pending_bids[:5], many=True, context={"request": request}
        ).data
        pending_bids_count = pending_bids.count()

        # Successful bids
        successful_bids = self.get_successful_bids(user=user)
        successful_bids_count = successful_bids.count()

        # Category counts
        category_counts = self.get_category_counts(user=user)

        return Response(
            data={
                "stats": {
                    "ongoing_auctions_count": ongoing_auctions_count,
                    "completed_auctions_count": completed_auctions_count,
                    "pending_bids_count": pending_bids_count,
                    "successful_bids_count": successful_bids_count,
                },
                "top_ongoing_auctions": top_ongoing_auctions,
                "top_pending_bids": top_pending_bids,
                "category_counts": category_counts,
            },
            status=HTTP_200_OK,
        )

    def get_ongoing_auctions(self, user):
        return Product.objects.filter(
            creator=user, valid_till__gte=datetime.now(tz=timezone.utc)
        ).order_by("valid_till")

    def get_completed_auctions(self, user):
        return Product.objects.filter(creator=user, is_sold=True)

    def get_pending_bids(self, user):
        return Bid.objects.select_related("product").filter(
            bidder=user, product__valid_till__gte=datetime.now(tz=timezone.utc)
        )

    def get_successful_bids(self, user):
        successful_bids = Bid.objects.select_related("product").filter(
            bidder=user,
            product__is_sold=True,
        )

        ids = [
            b.id
            for b in successful_bids.all()
            if b.product.highest_bid != None and b.product.highest_bid.bidder == user
        ]

        successful_bids = successful_bids.filter(pk__in=ids)

        return successful_bids

    def get_category_counts(self, user):
        products = Product.objects.filter(creator=user)
        total_product_count = products.count()
        category_counts = products.values("category__id", "category__title").annotate(
            product_count=Count("id"),
            category_percentage=ExpressionWrapper(
                F("product_count") * 100 / total_product_count,
                output_field=DecimalField(max_digits=5, decimal_places=2),
            ),
        )
        return category_counts
