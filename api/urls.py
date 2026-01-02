"""
API URL 라우팅 설정

이 모듈은 모든 API 엔드포인트의 URL 패턴을 정의합니다.
RESTful API 구조를 따르며 버전 관리를 지원합니다.

주요 기능:
- API 버전 관리
- RESTful URL 구조
- 엔드포인트 그룹화
"""

from django.urls import path, include
from . import views

# API v1 URL 패턴
urlpatterns_v1 = [
    # 공지사항 API
    path('notices/', views.NoticeAPIView.as_view(), name='api_notice_list'),
    path('notices/<int:pk>/', views.NoticeAPIView.as_view(), name='api_notice_detail'),
    
    # 기술 관리 API
    path('technologies/', views.TechnologyAPIView.as_view(), name='api_technology_list'),
    path('technologies/<int:pk>/', views.TechnologyAPIView.as_view(), name='api_technology_detail'),
    
    # 통합 검색 API
    path('search/', views.SearchAPIView.as_view(), name='api_search'),
    
    # 통계 API
    path('stats/', views.StatsAPIView.as_view(), name='api_stats'),
    
    # 헬스체크 API
    path('health/', views.StatsAPIView.as_view(), name='api_health'),
]

# 메인 API URL 패턴
urlpatterns = [
    path('v1/', include(urlpatterns_v1)),
]
