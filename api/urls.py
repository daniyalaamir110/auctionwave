from django.urls import path
from .views import CategoryListApiView, ProductListApiView

app_name = "api"

urlpatterns = [
    path("category", CategoryListApiView.as_view()),
    path("product", ProductListApiView.as_view())
]