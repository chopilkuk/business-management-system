# =============================================================================
# 비즈니스 관리 시스템 홈 앱 뷰
# =============================================================================
# 설명: 홈페이지 및 주요 기능 페이지들의 뷰 함수를 정의
# 작성자: 비즈니스 관리 시스템 개발팀
# 버전: 1.0.0
# =============================================================================

# Django 렌더링 함수 임포트
from django.shortcuts import render

def home(request):
    """
    홈 페이지 뷰 함수
    
    Args:
        request (HttpRequest): 클라이언트의 HTTP 요청 객체
        
    Returns:
        HttpResponse: 렌더링된 홈 페이지 HTML 응답
        
    Description:
        - 메인 대시보드 페이지를 렌더링
        - 사용자 정보, 업무 현황, 알림 등 표시
        - 네비게이션 메뉴 및 아이콘 링크 포함
    """
    return render(request, 'home.html')

def calendar(request):
    """
    캘린더 페이지 뷰 함수
    
    Args:
        request (HttpRequest): 클라이언트의 HTTP 요청 객체
        
    Returns:
        HttpResponse: 렌더링된 캘린더 페이지 HTML 응답
        
    Description:
        - 월간 캘린더 기능을 제공
        - 일정 추가, 수정, 삭제 기능
        - 이전/다음 달로 이동 가능
        - 오늘 날짜 강조 표시
    """
    return render(request, 'home/calendar.html')

def data(request):
    """
    자료실 페이지 뷰 함수
    
    Args:
        request (HttpRequest): 클라이언트의 HTTP 요청 객체
        
    Returns:
        HttpResponse: 렌더링된 자료실 페이지 HTML 응답
        
    Description:
        - 파일 업로드 및 다운로드 기능
        - 파일 검색 및 필터링
        - 파일 카테고리별 관리
        - 파일 공유 및 권한 설정
    """
    return render(request, 'home/data.html')

def authority(request):
    """
    권한 관리 페이지 뷰 함수
    
    Args:
        request (HttpRequest): 클라이언트의 HTTP 요청 객체
        
    Returns:
        HttpResponse: 렌더링된 권한 관리 페이지 HTML 응답
        
    Description:
        - 사용자 목록 표시 및 관리
        - 역할별 권한 설정 (관리자, 매니저, 사용자)
        - 사용자 추가, 수정, 삭제 기능
        - 접근 권한 제어
    """
    return render(request, 'home/authority.html')

def setting(request):
    """
    설정 페이지 뷰 함수
    
    Args:
        request (HttpRequest): 클라이언트의 HTTP 요청 객체
        
    Returns:
        HttpResponse: 렌더링된 설정 페이지 HTML 응답
        
    Description:
        - 사용자 개인 정보 설정
        - 알림 설정 관리
        - 테마 및 외관 설정
        - 데이터 백업 및 복원
    """
    return render(request, 'home/setting.html')

def address(request):
    """
    주소록 페이지 뷰 함수
    
    Args:
        request (HttpRequest): 클라이언트의 HTTP 요청 객체
        
    Returns:
        HttpResponse: 렌더링된 주소록 페이지 HTML 응답
        
    Description:
        - 연락처 목록 표시 및 관리
        - 연락처 검색 및 필터링
        - 연락처 추가, 수정, 삭제
        - 그룹별 연락처 관리
    """
    return render(request, 'home/address.html')
