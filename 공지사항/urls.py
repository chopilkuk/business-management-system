"""
공지사항 앱의 URL 라우팅 설정

이 모듈은 공지사항 관리를 위한 모든 URL 패턴을 정의합니다.
각 URL은 해당하는 뷰 함수와 매핑됩니다.

주요 기능:
- 공지사항 목록 페이지
- 공지사항 상세 페이지
- 공지사항 작성/수정/삭제
- 공지사항 게시/보관 기능
"""

# Django의 URL 경로 기능 임포트
from django.urls import path
# 현재 앱의 뷰 함수 임포트
from . import views


# 공지사항 앱의 URL 패턴 정의
urlpatterns = [
    # 공지사항 메인 페이지 (목록)
    path('', views.index, name='index'),
    
    # 공지사항 상세 페이지
    path('<int:pk>/', views.notice_detail, name='notice_detail'),
    
    # 공지사항 작성 페이지
    path('write/', views.noticewrite, name='noticewrite'),
    
    # 공지사항 수정 페이지
    path('<int:pk>/edit/', views.notice_edit, name='notice_edit'),
    
    # 공지사항 삭제 확인 페이지
    path('<int:pk>/delete/', views.notice_delete, name='notice_delete'),
    
    # 공지사항 게시 기능
    path('<int:pk>/publish/', views.notice_publish, name='notice_publish'),
    
    # 공지사항 보관 기능
    path('<int:pk>/archive/', views.notice_archive, name='notice_archive'),
]
