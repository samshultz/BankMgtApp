from django.urls import path
from .views import DashboardView

app_name = "bankapp"


urlpatterns = [
    path("accounts/dashboard/", DashboardView.as_view(), name="dashboard"),
]