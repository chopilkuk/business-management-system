
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
        
    from django.shortcuts import render, redirect, get_object_or_404
    from django.contrib import messages

    # 현재 앱의 모델 및 폼 임포트
    from .models import customer_information
    from .forms import CustomerInformationForm


    def index(request):
        """거래처 목록 페이지"""
        clients = customer_information.objects.all().order_by('-registration_date')
        return render(request, 'client_inform.html', {'clients': clients})


    def create(request):
        """거래처 생성 뷰"""
        if request.method == 'POST':
            form = CustomerInformationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, '거래처가 등록되었습니다.')
                return redirect('client_inform:index')
        else:
            form = CustomerInformationForm()
        return render(request, 'client_inform_form.html', {'form': form, 'action': '등록'})


    def edit(request, pk):
        """거래처 수정 뷰"""
        obj = get_object_or_404(customer_information, pk=pk)
        if request.method == 'POST':
            form = CustomerInformationForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                messages.success(request, '거래처가 수정되었습니다.')
                return redirect('client_inform:index')
        else:
            form = CustomerInformationForm(instance=obj)
        return render(request, 'client_inform_form.html', {'form': form, 'action': '수정'})


    def delete(request, pk):
        """거래처 삭제 확인/처리 뷰"""
        obj = get_object_or_404(customer_information, pk=pk)
        if request.method == 'POST':
            obj.delete()
            messages.success(request, '거래처가 삭제되었습니다.')
            return redirect('client_inform:index')
        return render(request, 'client_inform_confirm_delete.html', {'object': obj})
