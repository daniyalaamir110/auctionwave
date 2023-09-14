from django.urls import path, include
from .views import (
    CategoryViewSet,
    ProductViewSet,
    BidViewSet,
)
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# App
app_name = "api"

# Routers
# 1. Category
category_router = routers.DefaultRouter()
category_router.register(r"categories", CategoryViewSet)

# 2. Product
product_router = routers.DefaultRouter()
product_router.register(r"products", ProductViewSet)

# 3. Bid
bid_router = routers.DefaultRouter()
bid_router.register(r"bids", BidViewSet)

# Urls
urlpatterns = [
    path("", include(category_router.urls)),
    path("", include(product_router.urls)),
    path("", include(bid_router.urls)),
]
