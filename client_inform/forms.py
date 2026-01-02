from django import forms
from django.core.validators import MinLengthValidator, RegexValidator
from .models import customer_information


class CustomerInformationForm(forms.ModelForm):
    """
    거래처 정보 폼
    
    거래처 정보 등록 및 수정에 사용되는 폼입니다.
    데이터 검증 및 위젯 커스터마이징을 포함합니다.
    """
    
    class Meta:
        model = customer_information
        fields = [
            'registration_date', 'region', 'division', 'company_name', 'representative',
            'business_registration_number', 'number_of_employees', 'annual_sales',
            'sectors', 'event', 'outsourcing_work_type', 'main_business',
            'contract_status', 'v3_contract_status', 'staff_in_charge', 'phone_number',
            'business_address', 'e_mail', 'erp_maintenance', 'erp_usage_status',
            'groupware', 'company_evaluation', 'note'
        ]
        widgets = {
            'registration_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
            'region': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '지역을 입력하세요 (예: 서울, 경기)'
                }
            ),
            'division': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '구분을 입력하세요 (예: 내부, 외부, 파트너)'
                }
            ),
            'company_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '기업명을 입력하세요',
                    'required': 'required'
                }
            ),
            'representative': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '대표자명을 입력하세요',
                    'required': 'required'
                }
            ),
            'business_registration_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '사업자등록번호를 입력하세요',
                    'required': 'required'
                }
            ),
            'number_of_employees': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '종업원수',
                    'min': '0'
                }
            ),
            'annual_sales': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '연간 매출액',
                    'min': '0'
                }
            ),
            'sectors': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '주요 업종을 입력하세요 (예: IT, 제조, 서비스)'
                }
            ),
            'event': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '종목 또는 특별 이벤트를 입력하세요'
                }
            ),
            'outsourcing_work_type': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '외주사 작업 유형을 입력하세요'
                }
            ),
            'main_business': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '주요업무 내용을 입력하세요'
                }
            ),
            'contract_status': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '계약 상태를 입력하세요 (예: 진행중, 완료, 만료)'
                }
            ),
            'v3_contract_status': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'V3 계약 상태 (O 또는 X)',
                    'maxlength': '1'
                }
            ),
            'staff_in_charge': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '담당직원을 입력하세요'
                }
            ),
            'phone_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '전화번호를 입력하세요'
                }
            ),
            'business_address': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '사업장 주소를 입력하세요'
                }
            ),
            'e_mail': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '이메일 주소를 입력하세요'
                }
            ),
            'erp_maintenance': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'ERP 유지보수 상태를 입력하세요'
                }
            ),
            'erp_usage_status': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'ERP 사용 현황을 입력하세요'
                }
            ),
            'groupware': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            ),
            'company_evaluation': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '업체 평가 (예: A, B, C)',
                    'maxlength': '1'
                }
            ),
            'note': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': '비고나 추가 메모를 입력하세요',
                    'rows': 3
                }
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 필수 필드 표시
        required_fields = ['company_name', 'representative', 'business_registration_number']
        for field_name in required_fields:
            self.fields[field_name].required = True
        
        # 필드 레이블 설정
        field_labels = {
            'registration_date': '등록일',
            'region': '지역',
            'division': '구분',
            'company_name': '기업명',
            'representative': '대표자명',
            'business_registration_number': '사업자등록번호',
            'number_of_employees': '종업원수',
            'annual_sales': '연간 매출액',
            'sectors': '업종',
            'event': '종목/이벤트',
            'outsourcing_work_type': '외주사 작업 유형',
            'main_business': '주요업무',
            'contract_status': '계약 상태',
            'v3_contract_status': 'V3 계약 상태',
            'staff_in_charge': '담당직원',
            'phone_number': '전화번호',
            'business_address': '사업장 주소',
            'e_mail': '이메일',
            'erp_maintenance': 'ERP 유지보수',
            'erp_usage_status': 'ERP 사용 현황',
            'groupware': '그룹웨어 사용',
            'company_evaluation': '업체 평가',
            'note': '비고'
        }
        
        for field_name, label in field_labels.items():
            if field_name in self.fields:
                self.fields[field_name].label = label
    
    def clean_company_name(self):
        """기업명 검증"""
        company_name = self.cleaned_data.get('company_name')
        
        if company_name:
            # 공백만 있는지 확인
            if company_name.strip() == '':
                raise forms.ValidationError('기업명에 내용이 포함되어야 합니다.')
            
            # 최소 길이 확인
            if len(company_name.strip()) < 2:
                raise forms.ValidationError('기업명은 최소 2자 이상이어야 합니다.')
            
            # 최대 길이 확인
            if len(company_name) > 32:
                raise forms.ValidationError('기업명은 32자 이하이어야 합니다.')
        
        return company_name.strip()
    
    def clean_representative(self):
        """대표자명 검증"""
        representative = self.cleaned_data.get('representative')
        
        if representative:
            # 공백만 있는지 확인
            if representative.strip() == '':
                raise forms.ValidationError('대표자명에 내용이 포함되어야 합니다.')
            
            # 최소 길이 확인
            if len(representative.strip()) < 2:
                raise forms.ValidationError('대표자명은 최소 2자 이상이어야 합니다.')
            
            # 특수문자 제거 (SQL 인젝션 방지)
            if any(char in representative.strip() for char in ['<', '>', '"', "'", '&', '=', ';', '--', '/*', '*/']):
                raise forms.ValidationError('대표자명에 허용되지 않는 문자가 포함되어 있습니다.')
            
            # 한글/영문/숫자만 허용
            import re
            if not re.match(r'^[가-힣a-zA-Z0-9\s]+$', representative.strip()):
                raise forms.ValidationError('대표자명은 한글, 영문, 숫자만 입력할 수 있습니다.')
        
        return representative.strip()
    
    def clean_business_registration_number(self):
        """사업자등록번호 검증"""
        brn = self.cleaned_data.get('business_registration_number')
        
        if brn:
            # 공백만 있는지 확인
            if brn.strip() == '':
                raise forms.ValidationError('사업자등록번호에 내용이 포함되어야 합니다.')
            
            # 형식 검증 (숫자와 하이픈만 허용)
            import re
            if not re.match(r'^[\d-]+$', brn.strip()):
                raise forms.ValidationError('사업자등록번호는 숫자와 하이픈만 포함할 수 있습니다.')
            
            # 길이 검증 (10자 또는 12자)
            clean_brn = brn.replace('-', '')
            if len(clean_brn) not in [10, 12]:
                raise forms.ValidationError('사업자등록번호는 10자 또는 12자여야 합니다.')
            
            # 사업자등록번호 유효성 검증 (간단한 검증)
            if len(clean_brn) == 10:
                # 10자 사업자등록번호 검증
                if not self._validate_brn_10(clean_brn):
                    raise forms.ValidationError('유효하지 않은 사업자등록번호입니다.')
            elif len(clean_brn) == 12:
                # 12자 사업자등록번호 검증
                if not self._validate_brn_12(clean_brn):
                    raise forms.ValidationError('유효하지 않은 사업자등록번호입니다.')
        
        return brn.strip()
    
    def _validate_brn_10(self, brn):
        """10자 사업자등록번호 유효성 검증"""
        try:
            # 사업자등록번호 유효성 검증 알고리즘
            check_digit = int(brn[0])
            multiply = 9
            total = 0
            
            for i in range(1, 10):
                total += int(brn[i]) * multiply
                multiply -= 1
            
            check_digit = (10 - (total % 10)) % 10
            
            return check_digit == int(brn[9])
        except:
            return False
    
    def _validate_brn_12(self, brn):
        """12자 사업자등록번호 유효성 검증"""
        try:
            # 사업자등록번호 유효성 검증 알고리즘
            multipliers = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 5, 7]
            total = 0
            
            for i in range(12):
                total += int(brn[i]) * multipliers[i]
            
            check_digit = (11 - (total % 11)) % 10
            
            return check_digit == int(brn[11])
        except:
            return False
    
    def clean_phone_number(self):
        """전화번호 검증"""
        phone = self.cleaned_data.get('phone_number')
        
        if phone:
            # 형식 검증
            import re
            if not re.match(r'^[\d-]+$', phone.strip()):
                raise forms.ValidationError('전화번호는 숫자와 하이픈만 포함할 수 있습니다.')
            
            # 전화번호 길이 검증 (최소 10자, 최대 15자)
            clean_phone = phone.replace('-', '')
            if len(clean_phone) < 10 or len(clean_phone) > 15:
                raise forms.ValidationError('전화번호는 10자에서 15자 사이여야 합니다.')
            
            # 휴대폰 번호 형식 검증
            if clean_phone.startswith('010'):
                # 휴대폰 번호인 경우 11자여야 함
                if len(clean_phone) != 11:
                    raise forms.ValidationError('휴대폰 번호는 11자여야 합니다.')
            elif clean_phone.startswith('02'):
                # 지역번호인 경우 10자 또는 11자여야 함
                if len(clean_phone) not in [10, 11]:
                    raise forms.ValidationError('지역번호는 10자 또는 11자여야 합니다.')
            else:
                # 일반 번호는 10자여야 함
                if len(clean_phone) != 10:
                    raise forms.ValidationError('일반 번호는 10자여야 합니다.')
        
        return phone.strip()
    
    def clean_e_mail(self):
        """이메일 검증"""
        email = self.cleaned_data.get('e_mail')
        
        if email:
            # 이메일 형식 검증은 Django의 EmailField가 자동으로 처리
            return email.lower().strip()
        
        return email
    
    def clean_number_of_employees(self):
        """종업원수 검증"""
        employees = self.cleaned_data.get('number_of_employees')
        
        if employees is not None and employees < 0:
            raise forms.ValidationError('종업원수는 0 이상이어야 합니다.')
        
        return employees
    
    def clean_annual_sales(self):
        """연간 매출액 검증"""
        sales = self.cleaned_data.get('annual_sales')
        
        if sales is not None and sales < 0:
            raise forms.ValidationError('연간 매출액은 0 이상이어야 합니다.')
        
        return sales
    
    def clean_v3_contract_status(self):
        """V3 계약 상태 검증"""
        v3_status = self.cleaned_data.get('v3_contract_status')
        
        if v3_status:
            v3_status = v3_status.upper()
            if v3_status not in ['O', 'X']:
                raise forms.ValidationError('V3 계약 상태는 O 또는 X만 입력할 수 있습니다.')
        
        return v3_status
    
    def clean_company_evaluation(self):
        """업체 평가 검증"""
        evaluation = self.cleaned_data.get('company_evaluation')
        
        if evaluation:
            evaluation = evaluation.upper()
            if evaluation not in ['A', 'B', 'C']:
                raise forms.ValidationError('업체 평가는 A, B, C만 입력할 수 있습니다.')
        
        return evaluation
    
    def clean(self):
        """전체 폼 검증"""
        cleaned_data = super().clean()
        
        # 비즈니스 로직 검증
        contract_status = cleaned_data.get('contract_status')
        v3_status = cleaned_data.get('v3_contract_status')
        erp_usage = cleaned_data.get('erp_usage_status')
        
        # 계약이 완료된 경우 ERP 사용 상태 확인
        if contract_status == '완료' and erp_usage and '사용' in erp_usage:
            raise forms.ValidationError('계약이 완료된 경우 ERP 사용 상태가 "사용"일 수 없습니다.')
        
        # V3 계약이 있는 경우 계약 상태 확인
        if v3_status == 'O' and not contract_status:
            raise forms.ValidationError('V3 계약이 있는 경우 계약 상태를 반드시 입력해야 합니다.')
        
        return cleaned_data


class CustomerInformationSearchForm(forms.Form):
    """
    거래처 정보 검색 폼
    
    거래처 정보 검색에 사용되는 폼입니다.
    """
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '기업명이나 대표자명으로 검색하세요',
                'autocomplete': 'off'
            }
        )
    )
    
    region = forms.CharField(
        max_length=32,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '지역으로 검색'
            }
        )
    )
    
    sectors = forms.CharField(
        max_length=32,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '업종으로 검색'
            }
        )
    )
    
    contract_status = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '계약 상태로 검색'
            }
        )
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 필드 레이블 설정
        self.fields['search'].label = '검색'
        self.fields['region'].label = '지역'
        self.fields['sectors'].label = '업종'
        self.fields['contract_status'].label = '계약 상태'
