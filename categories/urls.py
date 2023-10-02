from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet

app_name = "categories"

category_router = DefaultRouter()
category_router.register("", CategoryViewSet)

urlpatterns = [path("", include(category_router.urls))]
