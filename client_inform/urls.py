
# Django URL 패턴 함수 임포트
from django.urls import path
# 현재 앱의 뷰 함수 임포트
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.index, name='index'),
]

app_name = 'client_inform'

urlpatterns += [
    path('create/', views.create, name='create'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/delete/', views.delete, name='delete'),
]
