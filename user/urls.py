from django.urls import path, include
from rest_framework import routers
from .views import RegisterView, UserViewSet

app_name = "user"

user_router = routers.DefaultRouter()
user_router.register(r"", UserViewSet)

urlpatterns = [
    path("", include(user_router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
]
