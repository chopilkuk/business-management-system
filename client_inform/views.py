# =============================================================================
# 비즈니스 관리 시스템 거래처 정보 관리 앱 뷰
# =============================================================================
# 설명: 거래처 정보 관리와 관련된 뷰 함수를 정의
# 작성자: 비즈니스 관리 시스템 개발팀
# 버전: 1.0.0
# =============================================================================

# Django 렌더링 함수 임포트
from django.shortcuts import render, redirect, get_object_or_404
# 현재 앱의 모델 임포트
from .models import customer_information
# 메시지 프레임워크 임포트
from django.contrib import messages

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

def add_client(request):
    """
    거래처 등록 뷰 함수
    
    거래처 등록 폼을 제공하고 데이터를 처리합니다.
    
    Args:
        request (HttpRequest): 클라이언트의 HTTP 요청 객체
        
    Returns:
        HttpResponse: 렌더링된 거래처 등록 페이지 HTML 응답
        
    Description:
        - GET 요청: 거래처 등록 폼 표시
        - POST 요청: 거래처 데이터 검증 및 저장
        - 성공 시 메시지 표시 후 목록으로 리다이렉트
    """
    if request.method == 'POST':
        # 폼 데이터 처리
        try:
            # 필수 필드들
            company_name = request.POST.get('company_name', '').strip()
            representative = request.POST.get('representative', '').strip()
            phone_number = request.POST.get('phone_number', '').strip()
            
            if not company_name:
                messages.error(request, '회사명은 필수 항목입니다.')
                return render(request, 'client_add.html')
            
            # 거래처 객체 생성
            client = customer_information.objects.create(
                company_name=company_name,
                representative=representative,
                phone_number=phone_number,
                business_registration_number=request.POST.get('business_registration_number', '').strip(),
                region=request.POST.get('region', '').strip(),
                division=request.POST.get('division', '').strip(),
                number_of_employees=request.POST.get('number_of_employees', ''),
                annual_sales=request.POST.get('annual_sales', ''),
                sectors=request.POST.get('sectors', '').strip(),
                event=request.POST.get('event', '').strip(),
                outsourcing_work_type=request.POST.get('outsourcing_work_type', '').strip(),
                main_business=request.POST.get('main_business', '').strip(),
                contract_status=request.POST.get('contract_status', '').strip(),
                v3_contract_status=request.POST.get('v3_contract_status', '').strip(),
                staff_in_charge=request.POST.get('staff_in_charge', '').strip(),
                business_address=request.POST.get('business_address', '').strip(),
                e_mail=request.POST.get('e_mail', '').strip(),
                erp_maintenance=request.POST.get('erp_maintenance', '').strip(),
                erp_usage_status=request.POST.get('erp_usage_status', '').strip(),
                groupware=request.POST.get('groupware', '').strip(),
                company_evaluation=request.POST.get('company_evaluation', '').strip(),
                note=request.POST.get('note', '').strip()
            )
            
            messages.success(request, f'거래처 "{company_name}"가 성공적으로 등록되었습니다.')
            return redirect('index')
            
        except Exception as e:
            messages.error(request, f'거래처 등록 중 오류가 발생했습니다: {str(e)}')
            return render(request, 'client_add.html')
    
    # GET 요청: 등록 폼 표시
    return render(request, 'client_add.html')

def client_detail(request, pk):
    """
    거래처 상세 정보 뷰 함수
    
    Args:
        request (HttpRequest): 클라이언트의 HTTP 요청 객체
        pk (int): 거래처의 기본키
        
    Returns:
        HttpResponse: 렌더링된 거래처 상세 페이지 HTML 응답
    """
    client = get_object_or_404(customer_information, pk=pk)
    return render(request, 'client_detail.html', {'client': client})

def edit_client(request, pk):
    """
    거래처 수정 뷰 함수
    
    Args:
        request (HttpRequest): 클라이언트의 HTTP 요청 객체
        pk (int): 거래처의 기본키
        
    Returns:
        HttpResponse: 렌더링된 거래처 수정 페이지 HTML 응답
    """
    client = get_object_or_404(customer_information, pk=pk)
    
    if request.method == 'POST':
        try:
            # 필드 업데이트
            client.company_name = request.POST.get('company_name', client.company_name).strip()
            client.representative = request.POST.get('representative', client.representative).strip()
            client.phone_number = request.POST.get('phone_number', client.phone_number).strip()
            client.business_registration_number = request.POST.get('business_registration_number', client.business_registration_number).strip()
            client.region = request.POST.get('region', client.region).strip()
            client.division = request.POST.get('division', client.division).strip()
            client.number_of_employees = request.POST.get('number_of_employees', client.number_of_employees)
            client.annual_sales = request.POST.get('annual_sales', client.annual_sales)
            client.sectors = request.POST.get('sectors', client.sectors).strip()
            client.event = request.POST.get('event', client.event).strip()
            client.outsourcing_work_type = request.POST.get('outsourcing_work_type', client.outsourcing_work_type).strip()
            client.main_business = request.POST.get('main_business', client.main_business).strip()
            client.contract_status = request.POST.get('contract_status', client.contract_status).strip()
            client.v3_contract_status = request.POST.get('v3_contract_status', client.v3_contract_status).strip()
            client.staff_in_charge = request.POST.get('staff_in_charge', client.staff_in_charge).strip()
            client.business_address = request.POST.get('business_address', client.business_address).strip()
            client.e_mail = request.POST.get('e_mail', client.e_mail).strip()
            client.erp_maintenance = request.POST.get('erp_maintenance', client.erp_maintenance).strip()
            client.erp_usage_status = request.POST.get('erp_usage_status', client.erp_usage_status).strip()
            client.groupware = request.POST.get('groupware', client.groupware).strip()
            client.company_evaluation = request.POST.get('company_evaluation', client.company_evaluation).strip()
            client.note = request.POST.get('note', client.note).strip()
            
            client.save()
            messages.success(request, f'거래처 "{client.company_name}"가 성공적으로 수정되었습니다.')
            return redirect('client_detail', pk=client.pk)
            
        except Exception as e:
            messages.error(request, f'거래처 수정 중 오류가 발생했습니다: {str(e)}')
    
    return render(request, 'client_edit.html', {'client': client})

def delete_client(request, pk):
    """
    거래처 삭제 뷰 함수
    
    Args:
        request (HttpRequest): 클라이언트의 HTTP 요청 객체
        pk (int): 거래처의 기본키
        
    Returns:
        HttpResponse: 렌더링된 거래처 삭제 확인 페이지 HTML 응답
    """
    client = get_object_or_404(customer_information, pk=pk)
    
    if request.method == 'POST':
        try:
            company_name = client.company_name
            client.delete()
            messages.success(request, f'거래처 "{company_name}"가 성공적으로 삭제되었습니다.')
            return redirect('index')
        except Exception as e:
            messages.error(request, f'거래처 삭제 중 오류가 발생했습니다: {str(e)}')
    
    return render(request, 'client_delete.html', {'client': client})
