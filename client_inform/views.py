# =============================================================================
# 비즈니스 관리 시스템 거래처 정보 관리 앱 뷰
# =============================================================================
# 설명: 거래처 정보 관리와 관련된 뷰 함수를 정의
# 작성자: 비즈니스 관리 시스템 개발팀
# 버전: 1.0.0
# =============================================================================

# Django 렌더링 함수 임포트
from django.shortcuts import render
# 현재 앱의 모델 임포트
from .models import customer_information

def index(request):
    """
    거래처 관리 메인 페이지 뷰 함수
    
    거래처 정보 관리 메인 페이지를 렌더링합니다.
    모든 거래처 목록을 등록일 최신순으로 표시합니다.
    
    Args:
        request (HttpRequest): 클라이언트의 HTTP 요청 객체
        
    Returns:
        HttpResponse: 렌더링된 거래처 관리 페이지 HTML 응답
        
    Description:
        - 거래처 관리 메인 페이지를 렌더링
        - 모든 거래처 목록을 데이터베이스에서 조회
        - 등록일 기준 내림차순 정렬 (최신순)
        - 거래처 정보 템플릿에 데이터 전달
        - 검색, 필터링, 정렬 기능 지원
        
    Database Query:
        - customer_information.objects.all(): 모든 거래처 레코드 조회
        - order_by('-registration_date'): 등록일 내림차순 정렬
        
    Template Context:
        - clients: 정렬된 거래처 목록 객체
    """
    # 모든 거래처를 데이터베이스에서 조회하여 등록일 최신순으로 정렬
    clients = customer_information.objects.all().order_by('-registration_date')
    
    # 거래처 관리 템플릿에 거래처 목록 데이터를 전달하여 렌더링
    return render(request, 'client_inform.html', {'clients': clients})
