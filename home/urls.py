# =============================================================================
# 비즈니스 관리 시스템 홈 앱 URL 설정
# =============================================================================
# 설명: 홈페이지 및 주요 기능 페이지들의 URL 패턴을 정의
# 작성자: 비즈니스 관리 시스템 개발팀
# 버전: 1.0.0
# =============================================================================

# Django URL 패턴 함수 임포트
from django.urls import path
# 현재 앱의 뷰 함수 임포트
from . import views

# =============================================================================
# URL 패턴 정의
# =============================================================================
# 각 URL 경로에 해당하는 뷰 함수를 매핑
urlpatterns = [
    # 홈페이지 - 메인 대시보드
    path('', views.home, name='home'),
    
    # 워크스페이스 - Untitled 스타일 대시보드
    path('workspace/', views.workspace, name='workspace'),
    
    # 완성형 홈페이지 - 완벽한 화면 비율
    path('complete/', views.home_complete, name='home_complete'),
    
    # 캘린더 페이지 - 일정 관리
    path('calendar/', views.calendar, name='calendar'),
    
    # 자료실 페이지 - 파일 관리
    path('data/', views.data, name='data'),
    
    # 권한 관리 페이지 - 사용자 권한 설정
    path('authority/', views.authority, name='authority'),
    
    # 설정 페이지 - 시스템 설정
    path('setting/', views.setting, name='setting'),
    
    # 주소록 페이지 - 연락처 관리
    path('address/', views.address, name='address'),
]
