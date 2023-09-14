from django.urls import path, include
from rest_framework import routers
from .views import RegisterView, UserViewSet

app_name = "user"

user_router = routers.DefaultRouter()
user_router.register("", UserViewSet)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("", include(user_router.urls)),
]
