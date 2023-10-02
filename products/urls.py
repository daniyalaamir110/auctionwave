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
    path("owned/", CurrentUserProductListView.as_view(), name="owned_list"),
    path(
        "owned/<int:pk>/",
        CurrentUserProductRetrieveView.as_view(),
        name="owned_detail",
    ),
    path(
        "owned/<int:pk>/bids/",
        UserProductBidsListView.as_view(),
        name="owned_bids_list",
    ),
]
