from django.urls import path
from . import views

urlpatterns = [
    path('', views.commute_main, name='commute_main'),
]
