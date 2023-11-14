from django.urls import path
from .views import DashboardRetrieveView

app_name = "dashboard"

urlpatterns = [
    path("", DashboardRetrieveView.as_view()),
]
