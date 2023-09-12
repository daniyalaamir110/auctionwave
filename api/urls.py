from django.urls import path
from .views import (
    CategoryListApiView,
    CategoryDetailApiView,
    ProductListApiView,
    LoginView,
    LogoutView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = "api"

urlpatterns = [
    # Auth views
    path("auth/login", TokenObtainPairView.as_view(), name="jwt_login"),
    path("auth/refresh", TokenRefreshView.as_view(), name="jwt_refresh"),
    # Category views
    path("category", CategoryListApiView.as_view()),
    path("category/<int:category_id>", CategoryDetailApiView.as_view()),
    # Product views
    path("product", ProductListApiView.as_view()),
]
