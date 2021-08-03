from django.urls import path

from . import views

app_name = 'drivers'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:driver_id>/', views.detail, name='detail'),
]