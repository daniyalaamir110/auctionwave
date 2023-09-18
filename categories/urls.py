from django.urls import path, include
from rest_framework import routers
from .views import CategoryViewSet

app_name = "categories"

category_router = routers.DefaultRouter()
category_router.register("", CategoryViewSet)

urlpatterns = [path("", include(category_router.urls))]
