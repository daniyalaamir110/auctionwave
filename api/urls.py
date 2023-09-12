from django.urls import path
from .views import (
    CategoryListApiView,
    CategoryDetailApiView,
    ProductListApiView,
    LoginView,
    LogoutView,
)

app_name = "api"

urlpatterns = [
    path("category", CategoryListApiView.as_view()),
    path("category/<int:category_id>", CategoryDetailApiView.as_view()),
    path("product", ProductListApiView.as_view()),
    path("auth/login", LoginView.as_view()),
    path("auth/logout", LogoutView.as_view()),
]
