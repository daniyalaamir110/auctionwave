from django.urls import path, include
from rest_framework import routers
from .views import (
    ProductCreateView,
    ProductListView,
    ProductRetrieveView,
    ProductDeleteView,
    CurrentUserProductListView,
    CurrentUserProductRetrieveView,
    ProductBidCreateView,
)

app_name = "products"

urlpatterns = [
    path("<int:pk>/", ProductRetrieveView.as_view(), name="retrieve_product"),
    path("", ProductListView.as_view(), name="list_products"),
    path("create/", ProductCreateView.as_view(), name="create_product"),
    path("delete/<int:pk>/", ProductDeleteView.as_view(), name="delete_product"),
    path("owned/", CurrentUserProductListView.as_view(), name="my_products"),
    path("owned/<int:pk>", CurrentUserProductRetrieveView.as_view(), name="my_product"),
    path(
        "<int:id>/bid",
        ProductBidCreateView.as_view(),
        name="product_bid_create",
    ),
]
