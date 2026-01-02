"""
API 모듈

이 모듈은 시스템의 RESTful API 기능을 제공합니다.
JSON 응답, 에러 처리, 인증 등을 포함합니다.
"""

# API 모듈 임포트
try:
    from .views import NoticeAPIView, TechnologyAPIView, SearchAPIView, StatsAPIView
    from .urls import urlpatterns
    
    # API 함수 내보내기
    __all__ = [
        'NoticeAPIView',
        'TechnologyAPIView', 
        'SearchAPIView',
        'StatsAPIView',
        'urlpatterns'
    ]
except ImportError:
    # Django 설정이 로드되지 않은 경우
    __all__ = []
