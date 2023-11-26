from django.urls import path
from .views import UserBidsListView, UserBidsDetailView

app_name = "bids"

urlpatterns = [
    path("", UserBidsListView.as_view(), name="list"),
    path("<int:pk>/", UserBidsDetailView.as_view(), name="detail"),
]
