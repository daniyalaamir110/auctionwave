from django.urls import path
from .views import (
    UserBidsListView,
    BidCreateView,
    UserBidsRetrieveView,
    UserBidsUpdateView,
    UserBidsDeleteView,
)

app_name = "bids"

urlpatterns = [
    path("", UserBidsListView.as_view(), name="user_bids_list"),
    path("create/", BidCreateView.as_view(), name="create_bid"),
    path("<int:pk>/", UserBidsRetrieveView.as_view(), name="user_bid_retrieve"),
    path("<int:pk>/edit", UserBidsUpdateView.as_view(), name="user_bid_update"),
    path("<int:pk>/cancel", UserBidsDeleteView.as_view(), name="user_bid_delete"),
]
