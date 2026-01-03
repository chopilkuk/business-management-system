# =============================================================================
# 비즈니스 관리 시스템 거래처 정보 관리 앱 관리자 설정
# =============================================================================
# 설명: Django 관리자 사이트에서 거래처 정보 모델을 관리하는 설정
# 작성자: 비즈니스 관리 시스템 개발팀
# 버전: 1.0.0
# =============================================================================

# Django 관리자 모듈 임포트
from django.contrib import admin

# =============================================================================
# 모델 임포트
# =============================================================================
# 현재 앱의 모델 임포트
from .models import customer_information

# =============================================================================
# 관리자 클래스 정의
# =============================================================================
@admin.register(customer_information)
class CustomerInformationAdmin(admin.ModelAdmin):
    """
    거래처 정보 관리자 클래스
    
    Django 관리자 사이트에서 거래처 정보 모델을 관리하는 설정을 정의합니다.
    목록 표시, 필터링, 검색, 정렬 등의 기능을 설정합니다.
    
    Attributes:
        list_display (list): 관리자 목록 페이지에 표시할 필드
        list_filter (list): 필터링 옵션을 제공할 필드
        search_fields (list): 검색 기능을 제공할 필드
        ordering (tuple): 기본 정렬 순서
        readonly_fields (tuple): 읽기 전용 필드
        
    Description:
        - 거래처 목록의 표시 형식 설정
        - 다양한 필터링 기능 제공 (지역, 구분, 계약 상태 등)
        - 복합 검색 기능 제공 (기업명, 대표자, 사업자등록번호)
        - 등록일 기준 내림차순 정렬
        - 관리자 사이트의 사용자 경험 최적화
    """
    
    # 관리자 목록 페이지에 표시할 필드 목록
    # 주요 정보를 순서대로 표시하여 정보 파악 용이
    list_display = [
        'company_name',           # 기업명 (핵심 식별자)
        'representative',         # 대표자명
        'business_registration_number',  # 사업자등록번호
        'region',                 # 지역
        'division',               # 구분
        'contract_status',       # 계약 상태
        'registration_date',     # 등록일
        'staff_in_charge',       # 담당자
    ]
    
    # 필터링 옵션을 제공할 필드 목록
    # 다양한 기준으로 거래처 필터링 기능 제공
    list_filter = [
        'region',                 # 지역별 필터링
        'division',               # 구분별 필터링
        'sectors',                # 업종별 필터링
        'contract_status',       # 계약 상태별 필터링
        'v3_contract_status',     # V3 계약 상태별 필터링
        'groupware',              # 그룹웨어 사용 여부별 필터링
        'company_evaluation',     # 업체 평가별 필터링
        'registration_date',      # 등록일별 필터링
    ]
    
    # 검색 기능을 제공할 필드 목록
    # 핵심 식별 정보를 기준으로 검색 기능 제공
    search_fields = [
        'company_name',                    # 기업명 검색
        'representative',                  # 대표자명 검색
        'business_registration_number',    # 사업자등록번호 검색
        'phone_number',                   # 전화번호 검색
        'e_mail',                         # 이메일 검색
        'staff_in_charge',                # 담당자 검색
    ]
    
    # 기본 정렬 순서
    # 등록일 최신순으로 정렬하여 최신 정보 우선 표시
    ordering = ('-registration_date',)
    
    # 읽기 전용 필드 목록
    # 일단 등록된 중요 정보는 수정하지 않도록 설정
    readonly_fields = (
        'registration_date',      # 등록일 (수정 불가)
    )
    
    # 목록 페이지에서 페이지당 표시할 레코드 수
    list_per_page = 25
    
    # 상세 페이지 필드셋 설정
    fieldsets = (
        ('기본 정보', {
            'fields': (
                'registration_date',
                'region',
                'division',
                'company_name',
                'representative',
                'business_registration_number',
            )
        }),
        ('비즈니스 정보', {
            'fields': (
                'number_of_employees',
                'annual_sales',
                'sectors',
                'event',
                'outsourcing_work_type',
                'main_business',
            )
        }),
        ('계약 정보', {
            'fields': (
                'contract_status',
                'v3_contract_status',
            )
        }),
        ('연락처 정보', {
            'fields': (
                'staff_in_charge',
                'phone_number',
                'business_address',
                'e_mail',
            )
        }),
        ('시스템 정보', {
            'fields': (
                'erp_maintenance',
                'erp_usage_status',
                'groupware',
            )
        }),
        ('평가 및 메모', {
            'fields': (
                'company_evaluation',
                'note',
            )
        }),
    )