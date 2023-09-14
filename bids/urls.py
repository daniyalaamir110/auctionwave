from django.urls import path, include
from rest_framework import routers
from .views import BidViewSet

app_name = "bids"

bid_router = routers.DefaultRouter()
bid_router.register("", BidViewSet)

urlpatterns = [path("", include(bid_router.urls))]
