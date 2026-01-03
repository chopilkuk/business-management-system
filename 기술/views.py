# =============================================================================
# 비즈니스 관리 시스템 기술 관리 앱 뷰
# =============================================================================
# 설명: 기술 관리와 관련된 뷰 함수를 정의
# 작성자: 비즈니스 관리 시스템 개발팀
# 버전: 1.0.0
# =============================================================================

# Django 렌더링 함수 임포트
from django.shortcuts import render
# 현재 앱의 모델 임포트
from .models import Technology

def index(request):
    """
    기술 관리 메인 페이지 뷰 함수
    
    기술 관리 메인 페이지를 렌더링합니다.
    모든 기술 목록을 생성일 최신순으로 표시합니다.
    
    Args:
        request (HttpRequest): 클라이언트의 HTTP 요청 객체
        
    Returns:
        HttpResponse: 렌더링된 기술 관리 페이지 HTML 응답
        
    Description:
        - 기술 관리 메인 페이지를 렌더링
        - 모든 기술 목록을 데이터베이스에서 조회
        - 생성일 기준 내림차순 정렬 (최신순)
        - 기술 정보 템플릿에 데이터 전달
        - 검색, 필터링, 정렬 기능 지원
        - 기술 카테고리별 분류 표시
        - 기술 난이도 및 상태 표시
        
    Database Query:
        - Technology.objects.all(): 모든 기술 레코드 조회
        - order_by('-created_at'): 생성일 내림차순 정렬
        
    Template Context:
        - technologies: 정렬된 기술 목록 객체
        
    Features:
        - 기술 목록 표시
        - 기술 검색 기능
        - 카테고리별 필터링
        - 기술 상태 관리
        - 기술 상세 정보 표시
        - 기술 관련 문서 링크
        
    Template:
        - technology.html: 기술 관리 메인 템플릿
    """
    # 모든 기술을 데이터베이스에서 조회하여 생성일 최신순으로 정렬
    technologies = Technology.objects.all().order_by('-created_at')
    
    # 기술 관리 템플릿에 기술 목록 데이터를 전달하여 렌더링
    return render(request, 'technology.html', {'technologies': technologies})
