"""
공지사항 앱의 뷰 함수

이 모듈은 공지사항 관리를 위한 모든 뷰 함수를 정의합니다.
사용자 요청을 처리하고, 데이터베이스와 상호작용하며, 템플릿을 렌더링합니다.

주요 기능:
- 공지사항 목록 표시 (검색, 필터링, 페이징)
- 공지사항 상세 정보 표시
- 공지사항 작성, 수정, 삭제
- 공지사항 게시 및 보관
- 권한 관리 및 에러 처리
"""

# Django의 단축 함수 임포트 (렌더링, 리다이렉트, 객체 가져오기)
from django.shortcuts import render, redirect, get_object_or_404
# 로그인 데코레이터 임포트 (인증된 사용자만 접근 가능)
from django.contrib.auth.decorators import login_required
# 메시지 프레임워크 임포트 (사용자 피드백 메시지)
from django.contrib import messages
# 페이지네이터 임포트 (페이지 나누기 기능)
from django.core.paginator import Paginator
# Q 객체 임포트 (복잡한 데이터베이스 쿼리)
from django.db.models import Q
# JSON 응답 임포트 (AJAX 요청 처리)
from django.http import JsonResponse
# 현재 앱의 모델 임포트
from .models import Notice
# 현재 앱의 폼 임포트
from .forms import NoticeForm


@login_required
def index(request):
    """
    공지사항 메인 페이지 뷰 함수
    
    공지사항 목록을 표시하는 메인 페이지입니다.
    검색, 필터링, 페이징 기능을 포함합니다.
    
    Args:
        request: HTTP 요청 객체
        
    Returns:
        HttpResponse: 렌더링된 공지사항 목록 페이지
    """
    # GET 파라미터에서 검색 및 필터링 값 가져오기
    search_query = request.GET.get('search', '')      # 검색어
    importance_filter = request.GET.get('importance', '')  # 중요도 필터
    status_filter = request.GET.get('status', '')        # 상태 필터
    
    # 모든 공지사항 가져오기
    notices = Notice.objects.all()
    
    # 검색 기능 적용 - 제목이나 내용에서 검색어 찾기
    if search_query:
        notices = notices.filter(
            Q(title__icontains=search_query) |  # 제목에서 검색 (대소문자 무관)
            Q(content__icontains=search_query)  # 내용에서 검색 (대소문자 무관)
        )
    
    # 중요도 필터링 적용
    if importance_filter:
        notices = notices.filter(importance=importance_filter)
    
    # 상태 필터링 적용
    if status_filter:
        notices = notices.filter(status=status_filter)
    
    # 일반 사용자는 게시된 공지만 볼 수 있도록 필터링
    if not request.user.is_staff:
        notices = notices.filter(status='published')
    
    # 페이지네이션 설정 - 페이지당 10개의 공지사항 표시
    paginator = Paginator(notices, 10)
    page_number = request.GET.get('page')  # 현재 페이지 번호 가져오기
    page_obj = paginator.get_page(page_number)  # 페이지 객체 가져오기
    
    # 템플릿에 전달할 컨텍스트 데이터
    context = {
        'page_obj': page_obj,  # 페이지네이션된 공지사항 객체
        'search_query': search_query,  # 현재 검색어
        'importance_filter': importance_filter,  # 현재 중요도 필터
        'status_filter': status_filter,  # 현재 상태 필터
        'importance_choices': Notice.IMPORTANCE_CHOICES,  # 중요도 선택지
        'status_choices': Notice.STATUS_CHOICES,  # 상태 선택지
    }
    
    # 공지사항 목록 템플릿 렌더링
    return render(request, 'notice.html', context)


@login_required
def notice_detail(request, pk):
    """
    공지사항 상세 페이지 뷰 함수
    
    특정 공지사항의 상세 정보를 표시합니다.
    조회수를 자동으로 증가시킵니다.
    
    Args:
        request: HTTP 요청 객체
        pk: 공지사항의 기본키
        
    Returns:
        HttpResponse: 렌더링된 공지사항 상세 페이지
    """
    # 기본키로 공지사항 객체 가져오기 (없으면 404 에러)
    notice = get_object_or_404(Notice, pk=pk)
    
    # 조회수 증가 (update_fields로 성능 최적화)
    notice.view_count += 1
    notice.save(update_fields=['view_count'])
    
    # 템플릿에 전달할 컨텍스트 데이터
    context = {
        'notice': notice,  # 공지사항 객체
    }
    
    # 공지사항 상세 템플릿 렌더링
    return render(request, 'notice_detail.html', context)


@login_required
def noticewrite(request):
    """
    공지사항 작성 페이지 뷰 함수
    
    새 공지사항을 작성하는 페이지입니다.
    폼 검증 및 에러 처리를 포함합니다.
    
    Args:
        request: HTTP 요청 객체
        
    Returns:
        HttpResponse: 렌더링된 공지사항 작성 페이지 또는 상세 페이지로 리다이렉트
    """
    # POST 요청인 경우 (폼 제출)
    if request.method == 'POST':
        # POST 데이터로 폼 객체 생성
        form = NoticeForm(request.POST)
        
        # 폼 유효성 검증
        if form.is_valid():
            # 폼 저장을 임시 중단 (작성자 설정을 위해)
            notice = form.save(commit=False)
            notice.author = request.user  # 현재 로그인한 사용자를 작성자로 설정
            
            # 자동 게시 옵션 확인
            if request.POST.get('auto_publish') == 'on':
                notice.status = 'published'  # 상태를 게시됨으로 변경
            
            # 공지사항 저장
            notice.save()
            
            # 성공 메시지 표시
            messages.success(request, '공지사항이 성공적으로 작성되었습니다.')
            
            # 작성된 공지사항 상세 페이지로 리다이렉트
            return redirect('notice_detail', pk=notice.pk)
        else:
            # 폼 검증 실패 시 에러 메시지 표시
            messages.error(request, '공지사항 작성에 실패했습니다. 다시 확인해주세요.')
    else:
        # GET 요청인 경우 (페이지 처음 로드)
        form = NoticeForm()  # 빈 폼 객체 생성
    
    # 템플릿에 전달할 컨텍스트 데이터
    context = {
        'form': form,  # 공지사항 폼 객체
        'title': '공지사항 작성',  # 페이지 제목
    }
    
    # 공지사항 작성 템플릿 렌더링
    return render(request, 'noticewrite.html', context)


@login_required
def notice_edit(request, pk):
    """
    공지사항 수정 페이지 뷰 함수
    
    기존 공지사항을 수정하는 페이지입니다.
    작성자 또는 관리자만 수정할 수 있습니다.
    
    Args:
        request: HTTP 요청 객체
        pk: 공지사항의 기본키
        
    Returns:
        HttpResponse: 렌더링된 공지사항 수정 페이지 또는 상세 페이지로 리다이렉트
    """
    # 기본키로 공지사항 객체 가져오기 (없으면 404 에러)
    notice = get_object_or_404(Notice, pk=pk)
    
    # 권한 확인 - 작성자 또는 관리자만 수정 가능
    if notice.author != request.user and not request.user.is_staff:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('notice_detail', pk=pk)
    
    # POST 요청인 경우 (폼 제출)
    if request.method == 'POST':
        # POST 데이터와 기존 객체로 폼 객체 생성
        form = NoticeForm(request.POST, instance=notice)
        
        # 폼 유효성 검증
        if form.is_valid():
            form.save()  # 폼 저장
            messages.success(request, '공지사항이 성공적으로 수정되었습니다.')
            return redirect('notice_detail', pk=notice.pk)
        else:
            messages.error(request, '공지사항 수정에 실패했습니다. 다시 확인해주세요.')
    else:
        # GET 요청인 경우 (페이지 처음 로드)
        form = NoticeForm(instance=notice)  # 기존 객체로 폼 생성
    
    # 템플릿에 전달할 컨텍스트 데이터
    context = {
        'form': form,  # 공지사항 폼 객체
        'notice': notice,  # 공지사항 객체
        'title': '공지사항 수정',  # 페이지 제목
    }
    
    # 공지사항 작성 템플릿 렌더링 (수정도 같은 템플릿 사용)
    return render(request, 'noticewrite.html', context)


@login_required
def notice_delete(request, pk):
    """
    공지사항 삭제 뷰 함수
    
    공지사항을 삭제하는 기능입니다.
    작성자 또는 관리자만 삭제할 수 있습니다.
    
    Args:
        request: HTTP 요청 객체
        pk: 공지사항의 기본키
        
    Returns:
        HttpResponse: 삭제 확인 페이지 또는 목록 페이지로 리다이렉트
    """
    # 기본키로 공지사항 객체 가져오기 (없으면 404 에러)
    notice = get_object_or_404(Notice, pk=pk)
    
    # 권한 확인 - 작성자 또는 관리자만 삭제 가능
    if notice.author != request.user and not request.user.is_staff:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('notice_detail', pk=pk)
    
    # POST 요청인 경우 (삭제 확인 후 실제 삭제)
    if request.method == 'POST':
        notice.delete()  # 공지사항 삭제
        messages.success(request, '공지사항이 성공적으로 삭제되었습니다.')
        return redirect('notice_index')  # 목록 페이지로 리다이렉트
    
    # 템플릿에 전달할 컨텍스트 데이터
    context = {
        'notice': notice,  # 공지사항 객체
    }
    
    # 삭제 확인 템플릿 렌더링
    return render(request, 'notice_confirm_delete.html', context)


@login_required
def notice_publish(request, pk):
    """
    공지사항 게시 뷰 함수
    
    공지사항을 게시 상태로 변경하는 기능입니다.
    작성자 또는 관리자만 게시할 수 있습니다.
    
    Args:
        request: HTTP 요청 객체
        pk: 공지사항의 기본키
        
    Returns:
        HttpResponse: 공지사항 상세 페이지로 리다이렉트
    """
    # 기본키로 공지사항 객체 가져오기 (없으면 404 에러)
    notice = get_object_or_404(Notice, pk=pk)
    
    # 권한 확인 - 작성자 또는 관리자만 게시 가능
    if notice.author != request.user and not request.user.is_staff:
        messages.error(request, '게시 권한이 없습니다.')
        return redirect('notice_detail', pk=pk)
    
    # 상태를 게시됨으로 변경 (update_fields로 성능 최적화)
    notice.status = 'published'
    notice.save(update_fields=['status'])
    
    messages.success(request, '공지사항이 성공적으로 게시되었습니다.')
    return redirect('notice_detail', pk=pk)


@login_required
def notice_archive(request, pk):
    """
    공지사항 보관 뷰 함수
    
    공지사항을 보관 상태로 변경하는 기능입니다.
    작성자 또는 관리자만 보관할 수 있습니다.
    
    Args:
        request: HTTP 요청 객체
        pk: 공지사항의 기본키
        
    Returns:
        HttpResponse: 공지사항 목록 페이지로 리다이렉트
    """
    # 기본키로 공지사항 객체 가져오기 (없으면 404 에러)
    notice = get_object_or_404(Notice, pk=pk)
    
    # 권한 확인 - 작성자 또는 관리자만 보관 가능
    if notice.author != request.user and not request.user.is_staff:
        messages.error(request, '보관 권한이 없습니다.')
        return redirect('notice_detail', pk=pk)
    
    # 상태를 보관됨으로 변경 (update_fields로 성능 최적화)
    notice.status = 'archived'
    notice.save(update_fields=['status'])
    
    messages.success(request, '공지사항이 성공적으로 보관되었습니다.')
    return redirect('notice_index')  # 목록 페이지로 리다이렉트
