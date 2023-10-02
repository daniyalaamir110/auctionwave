from django.urls import path
from .views import (
    UserListView,
    UserMeDetailView,
    UserUpdatePasswordView,
    UserRetrieveView,
)

app_name = "user"

urlpatterns = [
    path("", UserListView.as_view(), name="list"),
    path("<int:pk>/", UserRetrieveView.as_view(), name="retrieve"),
    path("me/", UserMeDetailView.as_view(), name="me"),
    path("me/password/", UserUpdatePasswordView.as_view(), name="me_password"),
]
