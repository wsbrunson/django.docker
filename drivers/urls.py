from django.urls import path

from . import views

app_name = "drivers"


urlpatterns = [
    path("", views.index, name="index"),
    path("populate/", views.populate_drivers, name="populate_drivers"),
    path(
        "populate-metrics/",
        views.populate_driver_twitter_metrics,
        name="populate_driver_twitter_metrics",
    ),
    path("remove-all/", views.remove_all_drivers, name="remove_all_drivers"),
    path("<str:driver_id>/", views.detail, name="detail"),
]
