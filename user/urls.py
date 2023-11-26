from django.urls import path
from .views import (
    UserListView,
    UserMeDetailView,
    UserUpdatePasswordView,
    UserDetailView,
    UsernameSuggestionView,
    UsernameAvailabilityView,
    EmailAvailabilityView,
    ProfileImageUpdateView,
)

app_name = "user"

urlpatterns = [
    path("", UserListView.as_view(), name="list"),
    path("<int:pk>/", UserDetailView.as_view(), name="retrieve"),
    path("me/", UserMeDetailView.as_view(), name="me"),
    path("me/password/", UserUpdatePasswordView.as_view(), name="me_password"),
    path(
        "me/profile_image/", ProfileImageUpdateView.as_view(), name="me_profile_image"
    ),
    path(
        "username-suggestions/",
        UsernameSuggestionView.as_view(),
        name="username_suggestion",
    ),
    path(
        "username-availability/",
        UsernameAvailabilityView.as_view(),
        name="username_availability",
    ),
    path(
        "email-availability/",
        EmailAvailabilityView.as_view(),
        name="email_availability",
    ),
]
