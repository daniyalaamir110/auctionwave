from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    CurrentUserProductListView,
    CurrentUserProductRetrieveView,
    ProductBidsListView,
    UserProductBidsListView,
)

app_name = "products"

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("<int:pk>/", ProductDetailView.as_view(), name="detail"),
    path("<int:pk>/bids/", ProductBidsListView.as_view(), name="bids_list"),
    path("my/", CurrentUserProductListView.as_view(), name="owned_list"),
    path(
        "my/<int:pk>/",
        CurrentUserProductRetrieveView.as_view(),
        name="owned_detail",
    ),
    path(
        "my/<int:pk>/bids/",
        UserProductBidsListView.as_view(),
        name="owned_bids_list",
    ),
]
