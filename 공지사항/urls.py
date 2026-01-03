# =============================================================================
# 비즈니스 관리 시스템 공지사항 앱 URL 설정
# =============================================================================
# 설명: 공지사항 관리와 관련된 URL 패턴을 정의
# 작성자: 비즈니스 관리 시스템 개발팀
# 버전: 1.0.0
# =============================================================================

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

# =============================================================================
# 임포트 구역
# =============================================================================
# Django의 URL 경로 기능 임포트
from django.urls import path
# 현재 앱의 뷰 함수 임포트
from . import views

# =============================================================================
# URL 패턴 정의
# =============================================================================
# 공지사항 앱의 모든 URL 패턴을 정의
urlpatterns = [
    # 공지사항 메인 페이지 (목록)
    # URL: /공지사항/ 또는 /공지사항
    # 뷰 함수: views.index
    # 이름: 'index' (템플릿에서 URL 역참에 사용)
    # 기능: 공지사항 목록 표시, 검색, 필터링, 페이지네이션
    path('', views.index, name='index'),
    
    # 공지사항 상세 페이지
    # URL: /공지사항/<pk>/ (pk는 공지사항의 기본키)
    # 뷰 함수: views.notice_detail
    # 이름: 'notice_detail' (템플릿에서 URL 역참에 사용)
    # 기능: 특정 공지사항의 상세 정보 표시, 조회수 증가
    path('<int:pk>/', views.notice_detail, name='notice_detail'),
    
    # 공지사항 작성 페이지
    # URL: /공지사항/write/
    # 뷰 함수: views.noticewrite
    # 이름: 'noticewrite' (템플릿에서 URL 역참에 사용)
    # 기능: 새 공지사항 작성 폼 제공, 데이터 검증 및 저장
    path('write/', views.noticewrite, name='noticewrite'),
    
    # 공지사항 수정 페이지
    # URL: /공지사항/<pk>/edit/ (pk는 공지사항의 기본키)
    # 뷰 함수: views.notice_edit
    # 이름: 'notice_edit' (템플릿에서 URL 역참에 사용)
    # 기능: 기존 공지사항 수정 폼 제공, 권한 확인, 데이터 업데이트
    path('<int:pk>/edit/', views.notice_edit, name='notice_edit'),
    
    # 공지사항 삭제 확인 페이지
    # URL: /공지사항/<pk>/delete/ (pk는 공지사항의 기본키)
    # 뷰 함수: views.notice_delete
    # 이름: 'notice_delete' (템플릿에서 URL 역참에 사용)
    # 기능: 공지사항 삭제 확인 페이지, 권한 확인, 데이터 삭제
    path('<int:pk>/delete/', views.notice_delete, name='notice_delete'),
    
    # 공지사항 게시 기능
    # URL: /공지사항/<pk>/publish/ (pk는 공지사항의 기본키)
    # 뷰 함수: views.notice_publish
    # 이름: 'notice_publish' (템플릿에서 URL 역참에 사용)
    # 기능: 공지사항 상태를 '게시됨'으로 변경, 권한 확인
    path('<int:pk>/publish/', views.notice_publish, name='notice_publish'),
    
    # 공지사항 보관 기능
    # URL: /공지사항/<pk>/archive/ (pk는 공지사항의 기본키)
    # 뷰 함수: views.notice_archive
    # 이름: 'notice_archive' (템플릿에서 URL 역참에 사용)
    # 기능: 공지사항 상태를 '보관됨'으로 변경, 권한 확인
    path('<int:pk>/archive/', views.notice_archive, name='notice_archive'),
]
