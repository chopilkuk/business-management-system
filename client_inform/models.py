"""
거래처 정보 관리 앱의 데이터베이스 모델

이 모듈은 거래처 정보 관리와 관련된 데이터베이스 모델을 정의합니다.
customer_information 모델은 거래처의 모든 주요 정보를 저장합니다.

주요 기능:
- 거래처 기본 정보 저장 (기업명, 대표자, 사업자등록번호 등)
- 비즈니스 정보 저장 (업종, 매출, 계약 상태 등)
- 시스템 정보 저장 (ERP 사용 여부, 담당자 등)
"""

from django.db import models

class customer_information(models.Model):
    """
    거래처 정보 모델
    
    이 모델은 거래처의 모든 정보를 저장하는 중앙 데이터 구조입니다.
    기업의 기본 정보부터 비즈니스 관련 정보, 시스템 사용 정보까지 포함합니다.
    
    Attributes:
        registration_date (Date): 거래처 등록일
        region (Char): 지역 정보
        division (Char): 구분 (예: 내부, 외부, 파트너 등)
        company_name (Char): 기업명 (필수)
        representative (Char): 대표자명 (필수)
        business_registration_number (Char): 사업자등록번호 (필수, 고유)
        number_of_employees (Integer): 종업원수
        annual_sales (Integer): 연간 매출액
        sectors (Char): 업종
        event (Char): 종목/이벤트
        outsourcing_work_type (Char): 외주사 작업 유형
        main_business (Char): 주요업무
        contract_status (Char): 계약 상태
        v3_contract_status (Char): V3 백신 계약 상태
        staff_in_charge (Char): 담당직원
        phone_number (Char): 전화번호
        business_address (Char): 사업장 주소
        e_mail (Char): 이메일 주소
        erp_maintenance (Char): ERP 유지보수 상태
        erp_usage_status (Char): ERP 사용 현황
        groupware (Boolean): 그룹웨어 사용 여부
        company_evaluation (Char): 업체 평가
        note (Char): 비고/메모
    """
    
    # 기본 정보 필드들
    registration_date = models.DateField('reg_date')  # 거래처 등록일
    region = models.CharField(max_length=32)           # 지역 (예: 서울, 경기 등)
    division = models.CharField(max_length=32)          # 구분 (예: 내부, 외부, 파트너)
    
    # 핵심 식별 정보 - 필수 필드
    company_name = models.CharField(max_length=32)      # 기업명 (거래처의 핵심 식별자)
    representative = models.CharField(max_length=32)     # 대표자명
    business_registration_number = models.CharField(max_length=32)  # 사업자등록번호
    
    # 비즈니스 규모 정보
    number_of_employees = models.IntegerField(default=0)  # 종업원수 (기본값: 0)
    annual_sales = models.IntegerField(default=0)          # 연간 매출액 (기본값: 0)
    
    # 비즈니스 상세 정보
    sectors = models.CharField(max_length=32)           # 주요 업종 (예: IT, 제조, 서비스 등)
    event = models.CharField(max_length=64)              # 종목 또는 특별 이벤트
    outsourcing_work_type = models.CharField(max_length=32)  # 외주사 작업 유형
    main_business = models.CharField(max_length=32)     # 주요업무 내용
    
    # 계약 관련 정보
    contract_status = models.CharField(max_length=100)  # 계약 상태 (예: 진행중, 완료, 만료 등)
    v3_contract_status = models.CharField(max_length=2)  # V3 백신 계약 상태 (예: O, X)
    
    # 담당자 및 연락처 정보
    staff_in_charge = models.CharField(max_length=32)     # 담당직원
    phone_number = models.CharField(max_length=50)       # 전화번호
    business_address = models.CharField(max_length=50)     # 사업장 주소
    e_mail = models.CharField(max_length=32)             # 이메일 주소
    
    # 시스템 사용 정보
    erp_maintenance = models.CharField(max_length=10)     # ERP 유지보수 상태
    erp_usage_status = models.CharField(max_length=8)     # ERP 사용 현황
    groupware = models.BooleanField()                    # 그룹웨어 사용 여부 (True/False)
    
    # 평가 및 메모
    company_evaluation = models.CharField(max_length=10)  # 업체 평가 (예: A, B, C 등급)
    note = models.CharField(max_length=200)               # 비고 또는 추가 메모

    class Meta:
        """
        모델 메타데이터 클래스
        
        이 클래스는 모델의 동작과 표현을 제어하는 설정을 포함합니다.
        """
        verbose_name = '거래처 정보'           # 단수 형태의 모델 이름 (관리자 사이트 등에서 표시)
        verbose_name_plural = '거래처 정보들'    # 복수 형태의 모델 이름
        ordering = ['-registration_date']      # 기본 정렬 순서 (등록일 최신순)
        
        # 제약 조건 설정
        constraints = [
            models.UniqueConstraint(
                fields=['business_registration_number'], 
                name='unique_business_registration_number'
            )  # 사업자등록번호 고유 제약 조건
        ]

    def __str__(self):
        """
        모델 인스턴스의 문자열 표현
        
        Returns:
            str: 기업명을 반환하여 관리자 사이트 등에서 식별하기 쉽게 함
        """
        return self.company_name

    def clean(self):
        """
        모델 유효성 검증
        
        이 메서드는 모델 저장 전에 자동으로 호출되어 데이터의 유효성을 검증합니다.
        비즈니스 로직에 따른 추가적인 검증 규칙을 구현할 수 있습니다.
        
        Raises:
            ValidationError: 데이터가 유효하지 않을 경우
        """
        from django.core.exceptions import ValidationError
        
        # 사업자등록번호 형식 검증 (간단한 검증)
        if self.business_registration_number:
            # 숫자와 하이픈만 허용
            import re
            if not re.match(r'^[\d-]+$', self.business_registration_number):
                raise ValidationError('사업자등록번호는 숫자와 하이픈만 포함할 수 있습니다.')
        
        # 이메일 형식 검증
        if self.e_mail:
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, self.e_mail):
                raise ValidationError('유효하지 않은 이메일 주소입니다.')
        
        # 종업원수와 매출액은 음수일 수 없음
        if self.number_of_employees < 0:
            raise ValidationError('종업원수는 0 이상이어야 합니다.')
        
        if self.annual_sales < 0:
            raise ValidationError('연간 매출액은 0 이상이어야 합니다.')

    def save(self, *args, **kwargs):
        """
        모델 저장 메서드
        
        데이터베이스에 모델을 저장하기 전에 추가적인 로직을 수행합니다.
        
        Args:
            *args: 위치 인자
            **kwargs: 키워드 인자
        """
        # 저장 전 자동화된 데이터 처리
        self.clean()  # 유효성 검증 실행
        
        # 등록일이 없으면 현재 날짜로 설정
        if not self.registration_date:
            from django.utils import timezone
            self.registration_date = timezone.now().date()
        
        # 문자열 필드의 공백 정리
        for field in ['company_name', 'representative', 'region', 'division']:
            value = getattr(self, field, None)
            if value:
                setattr(self, field, value.strip())
        
        super().save(*args, **kwargs)  # 실제 저장 실행

    @property
    def get_full_address(self):
        """
        완전한 주소 반환 프로퍼티
        
        Returns:
            str: 사업장 주소를 반환하거나, 없으면 '주소 정보 없음' 반환
        """
        return self.business_address if self.business_address else '주소 정보 없음'
    
    @property
    def is_active_contract(self):
        """
        활성 계약 여부 확인 프로퍼티
        
        Returns:
            bool: 계약 상태가 '진행중'이면 True, 아니면 False
        """
        return self.contract_status == '진행중'
    
    @property
    def has_v3_contract(self):
        """
        V3 계약 여부 확인 프로퍼티
        
        Returns:
            bool: V3 계약 상태가 'O'이면 True, 아니면 False
        """
        return self.v3_contract_status == 'O'
    
    @property
    def get_employee_count_display(self):
        """
        종업원수 표시 포맷 프로퍼티
        
        Returns:
            str: 종업원수를 포맷팅하여 반환 (예: '50명')
        """
        return f"{self.number_of_employees}명" if self.number_of_employees > 0 else "미정보"
    
    @property
    def get_sales_display(self):
        """
        매출액 표시 포맷 프로퍼티
        
        Returns:
            str: 매출액을 포맷팅하여 반환 (예: '10억원')
        """
        if self.annual_sales > 0:
            if self.annual_sales >= 100000000:  # 1억 이상
                return f"{self.annual_sales // 100000000}억원"
            elif self.annual_sales >= 10000:  # 1천만 이상
                return f"{self.annual_sales // 10000}천만원"
            else:
                return f"{self.annual_sales:,}원"
        return "미정보"