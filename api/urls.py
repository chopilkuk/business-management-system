# =============================================================================
# 비즈니스 관리 시스템 RESTful API URL 설정
# =============================================================================
# 설명: 모든 API 엔드포인트의 URL 패턴을 정의
# 작성자: 비즈니스 관리 시스템 개발팀
# 버전: 1.0.0
# =============================================================================

"""
API URL 라우팅 설정

이 모듈은 모든 API 엔드포인트의 URL 패턴을 정의합니다.
RESTful API 구조를 따르며 버전 관리를 지원합니다.

주요 기능:
- API 버전 관리
- RESTful URL 구조
- 엔드포인트 그룹화
"""

# =============================================================================
# 임포트 구역
# =============================================================================
# Django URL 패턴 및 인클루드 함수 임포트
from django.urls import path, include
# 현재 앱의 뷰 함수 임포트
from . import views

# =============================================================================
# API v1 URL 패턴 정의
# =============================================================================
# API 버전 1의 모든 엔드포인트를 정의
urlpatterns_v1 = [
    # =============================================================================
    # 공지사항 API 엔드포인트
    # =============================================================================
    # 공지사항 목록 및 생성 API
    # URL: /api/v1/notices/
    # 뷰: views.NoticeAPIView.as_view()
    # 이름: 'api_notice_list'
    # 기능: GET (목록 조회), POST (공지사항 생성)
    path('notices/', views.NoticeAPIView.as_view(), name='api_notice_list'),
    
    # 공지사항 상세, 수정, 삭제 API
    # URL: /api/v1/notices/<pk>/ (pk는 공지사항의 기본키)
    # 뷰: views.NoticeAPIView.as_view()
    # 이름: 'api_notice_detail'
    # 기능: GET (상세 조회), PUT (수정), DELETE (삭제)
    path('notices/<int:pk>/', views.NoticeAPIView.as_view(), name='api_notice_detail'),
    
    # =============================================================================
    # 기술 관리 API 엔드포인트
    # =============================================================================
    # 기술 목록 및 생성 API
    # URL: /api/v1/technologies/
    # 뷰: views.TechnologyAPIView.as_view()
    # 이름: 'api_technology_list'
    # 기능: GET (목록 조회), POST (기술 생성)
    path('technologies/', views.TechnologyAPIView.as_view(), name='api_technology_list'),
    
    # 기술 상세, 수정, 삭제 API
    # URL: /api/v1/technologies/<pk>/ (pk는 기술의 기본키)
    # 뷰: views.TechnologyAPIView.as_view()
    # 이름: 'api_technology_detail'
    # 기능: GET (상세 조회), PUT (수정), DELETE (삭제)
    path('technologies/<int:pk>/', views.TechnologyAPIView.as_view(), name='api_technology_detail'),
    
    # =============================================================================
    # 통합 검색 API 엔드포인트
    # =============================================================================
    # 통합 검색 API
    # URL: /api/v1/search/
    # 뷰: views.SearchAPIView.as_view()
    # 이름: 'api_search'
    # 기능: GET (공지사항, 기술, 거래처 통합 검색)
    # 파라미터: q (검색어), type (검색 타입), page (페이지), per_page (페이지당 항목 수)
    path('search/', views.SearchAPIView.as_view(), name='api_search'),
    
    # =============================================================================
    # 통계 API 엔드포인트
    # =============================================================================
    # 시스템 통계 API
    # URL: /api/v1/stats/
    # 뷰: views.StatsAPIView.as_view()
    # 이름: 'api_stats'
    # 기능: GET (공지사항, 기술, 거래처 통계 데이터)
    path('stats/', views.StatsAPIView.as_view(), name='api_stats'),
    
    # =============================================================================
    # 헬스체크 API 엔드포인트
    # =============================================================================
    # API 헬스체크
    # URL: /api/v1/health/
    # 뷰: views.StatsAPIView.as_view()
    # 이름: 'api_health'
    # 기능: GET (API 상태 확인, 시스템 건강 상태 점검)
    path('health/', views.StatsAPIView.as_view(), name='api_health'),
]

# =============================================================================
# 메인 API URL 패턴 정의
# =============================================================================
# API의 메인 진입점을 정의하고 버전 관리를 적용
urlpatterns = [
    # API v1 버전 진입점
    # URL: /api/v1/
    # 기능: v1 버전의 모든 API 엔드포인트를 포함
    path('v1/', include(urlpatterns_v1)),
]
