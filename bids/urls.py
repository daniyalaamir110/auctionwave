from django.urls import path, include
from rest_framework import routers
from .views import UserBidsListView

app_name = "bids"

urlpatterns = [path("", UserBidsListView.as_view(), name="user_bids_list")]
