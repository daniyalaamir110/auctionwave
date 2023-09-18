from django.urls import path, include
from rest_framework import routers
from .views import (
    ProductCreateView,
    ProductListView,
    ProductRetrieveView,
    ProductDeleteView,
    CurrentUserProductListView,
    CurrentUserProductRetrieveView,
    ProductBidsListView,
    UserProductBidsListView,
)

app_name = "products"

urlpatterns = [
    path("", ProductListView.as_view(), name="list_product"),
    path("<int:pk>/", ProductRetrieveView.as_view(), name="retrieve_product"),
    path("<int:pk>/bids", ProductBidsListView.as_view(), name="product_bids_list"),
    path("create/", ProductCreateView.as_view(), name="create_product"),
    path("delete/<int:pk>/", ProductDeleteView.as_view(), name="delete_product"),
    path("owned/", CurrentUserProductListView.as_view(), name="my_products"),
    path(
        "owned/<int:pk>",
        CurrentUserProductRetrieveView.as_view(),
        name="my_product_bids_list",
    ),
    path(
        "owned/<int:pk>/bids",
        UserProductBidsListView.as_view(),
        name="my_product",
    ),
]
