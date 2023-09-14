from django.urls import path, include
from rest_framework import routers
from .views import (
    ProductCreateView,
    ProductListView,
    ProductRetrieveView,
    ProductDeleteView,
)

app_name = "products"

product_router = routers.DefaultRouter()
product_router.register("", ProductCreateView)

# urlpatterns = [path("", include(product_router.urls))]
urlpatterns = [
    path("<int:pk>/", ProductRetrieveView.as_view(), name="retrieve_product"),
    path("", ProductListView.as_view(), name="list_products"),
    path("create/", ProductCreateView.as_view(), name="create_product"),
    path("delete/<int:pk>/", ProductDeleteView.as_view(), name="delete_product"),
]
