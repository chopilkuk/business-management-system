from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('calendar/', views.calendar, name='calendar'),
    path('data/', views.data, name='data'),
    path('authority/', views.authority, name='authority'),
    path('setting/', views.setting, name='setting'),
    path('address/', views.address, name='address'),
]
