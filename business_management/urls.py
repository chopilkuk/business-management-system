"""
URL configuration for business_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('login/', include('login.urls')),
    path('client_inform/', include('client_inform.urls')),
    path('client/', include('client_inform.urls')),
    path('businessStatus/', include('businessStatus.urls')),
    path('businessManagement/', include('businessStatus.urls')),
    path('commute/', include('commute.urls')),
    path('공지사항/', include('공지사항.urls')),
    path('기술/', include('기술.urls')),
    path('technology/', include('기술.urls')),
    path('cooperation/', include('commute.urls')),
    path('calendar/', include('home.urls')),
    path('data/', include('home.urls')),
    path('authority/', include('home.urls')),
    path('setting/', include('home.urls')),
    path('address/', include('home.urls')),
    path('주소/', include('home.urls')),
    path('notice/', include('공지사항.urls')),
    path('supportProject/', include('home.urls')),
    
    # API 엔드포인트
    path('api/', include('api.urls')),
    
    # 헬스체크 엔드포인트
    path('health/', include('api.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
