from django.urls import path

from . import views

app_name = "drivers"


urlpatterns = [
    path("v1/", views.index, name="index"),
    path("v1/metrics", views.all_driver_metrics, name="all_driver_metrics"),
    path("v1/metrics/<str:driver_id>/", views.driver_metrics, name="driver_metrics"),
    path("v1/<str:driver_id>/", views.detail, name="detail"),
]
