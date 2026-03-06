# =============================================================================
# 비즈니스 관리 시스템 거래처 정보 관리 앱 URL 설정
# =============================================================================
# 설명: 거래처 정보 관리와 관련된 URL 패턴을 정의
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
    # 거래처 정보 관리 메인 페이지
    # URL: /client_inform/ 또는 /client_inform
    # 뷰 함수: views.index
    # 이름: 'index' (템플릿에서 URL 역참에 사용)
    path('', views.index, name='index'),
    
    # 거래처 등록 페이지
    # URL: /client_inform/add/
    # 뷰 함수: views.add_client
    # 이름: 'add_client' (템플릿에서 URL 역참에 사용)
    path('add/', views.add_client, name='add_client'),
    
    # 거래처 상세 페이지
    # URL: /client_inform/<pk>/
    # 뷰 함수: views.client_detail
    # 이름: 'client_detail' (템플릿에서 URL 역참에 사용)
    path('<int:pk>/', views.client_detail, name='client_detail'),
    
    # 거래처 수정 페이지
    # URL: /client_inform/<pk>/edit/
    # 뷰 함수: views.edit_client
    # 이름: 'edit_client' (템플릿에서 URL 역참에 사용)
    path('<int:pk>/edit/', views.edit_client, name='edit_client'),
    
    # 거래처 삭제
    # URL: /client_inform/<pk>/delete/
    # 뷰 함수: views.delete_client
    # 이름: 'delete_client' (템플릿에서 URL 역참에 사용)
    path('<int:pk>/delete/', views.delete_client, name='delete_client'),
]
