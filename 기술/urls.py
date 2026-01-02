"""
기술 관리 앱의 URL 라우팅 설정

이 모듈은 기술 관리를 위한 모든 URL 패턴을 정의합니다.
각 URL은 해당하는 뷰 함수와 매핑됩니다.

주요 기능:
- 기술 목록 페이지
- 기술 상세 페이지
- 기술 등록/수정/삭제
- 기술 검색 및 필터링
"""

# Django의 URL 경로 기능 임포트
from django.urls import path
# 현재 앱의 뷰 함수 임포트
from . import views


# 기술 관리 앱의 URL 패턴 정의
urlpatterns = [
    # 기술 메인 페이지 (목록)
    path('', views.index, name='index'),
    
    # 기술 상세 페이지
    # path('<int:pk>/', views.technology_detail, name='technology_detail'),
    
    # 기술 등록 페이지
    # path('create/', views.technology_create, name='technology_create'),
    
    # 기술 수정 페이지
    # path('<int:pk>/edit/', views.technology_edit, name='technology_edit'),
    
    # 기술 삭제 확인 페이지
    # path('<int:pk>/delete/', views.technology_delete, name='technology_delete'),
]
