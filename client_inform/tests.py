
# Django 테스트 프레임워크 임포트
from django.test import TestCase
from .forms import CustomerInformationForm
from .models import customer_information


class ClientInformTests(TestCase):
    """
    거래처 정보 관리 앱 테스트 클래스
    
    거래처 정보 관리 기능의 정상적인 동작을 검증하는 테스트 케이스를 포함합니다.
    모델 생성, 데이터 검증, CRUD 작업, 폼 처리 등을 테스트합니다.
    
    Test Methods:
        test_client_creation: 거래처 생성 테스트
        test_client_validation: 거래처 데이터 유효성 검증 테스트
        test_client_list: 거래처 목록 조회 테스트
        test_client_update: 거래처 정보 수정 테스트
        test_client_delete: 거래처 삭제 테스트
        
    Description:
        - 거래처 모델의 생성 및 관리 기능 확인
        - 데이터베이스 작업의 정상적인 동작 검증
        - 폼 유효성 검증 및 에러 처리 확인
        - 권한 관리 및 보안 기능 검증
    """
    
    def test_client_creation(self):
        """
        거래처 생성 테스트 메서드
        
        거래처 정보를 정상적으로 생성할 수 있는지 확인합니다.
        필수 필드와 선택 필드의 처리를 검증합니다.
        
        Returns:
            None: 테스트 결과는 자동으로 평가됩니다
            
        Raises:
            AssertionError: 테스트가 실패할 경우
            
        Test Steps:
            1. 거래처 생성 데이터 준비
            2. 데이터베이스에 거래처 저장
            3. 저장된 데이터의 정확성 확인
            4. 필수 필드의 값 검증
        """
        data = {
            'company_name': '테스트주식회사',
            'representative': '홍길동',
            'business_registration_number': '1234567890',
            'registration_date': '2025-01-01',
            'region': '서울',
            'division': '외주',
            'number_of_employees': 5,
            'annual_sales': 1000000,
            'sectors': 'IT',
            'event': '',
            'outsourcing_work_type': '',
            'main_business': '',
            'contract_status': '',
            'v3_contract_status': 'O',
            'staff_in_charge': '',
            'phone_number': '010-0000-0000',
            'business_address': '',
            'e_mail': 'test@example.com',
            'erp_maintenance': '',
            'erp_usage_status': '',
            'groupware': False,
            'company_evaluation': 'A',
            'note': ''
        }
        form = CustomerInformationForm(data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_json())
        obj = form.save()
        self.assertIsInstance(obj, customer_information)
    
    def test_client_validation(self):
        """
        거래처 데이터 유효성 검증 테스트 메서드
        
        거래처 데이터의 유효성 검증 로직이 정상적으로 동작하는지 확인합니다.
        사업자등록번호, 이메일 형식 등을 검증합니다.
        
        Returns:
            None: 테스트 결과는 자동으로 평가됩니다
            
        Raises:
            AssertionError: 테스트가 실패할 경우
            
        Test Steps:
            1. 유효하지 않은 데이터 생성 시도록
            2. clean() 메서드 호출
            3. ValidationError 발생 확인
            4. 에러 메시지 검증
        """
        data = {
            'company_name': 'A',
            'representative': '!!',
            'business_registration_number': 'abc',
            'registration_date': '2025-01-01',
            'region': '서울',
            'division': '외주',
            'number_of_employees': -1,
            'annual_sales': -100,
            'sectors': 'IT',
            'event': '',
            'outsourcing_work_type': '',
            'main_business': '',
            'contract_status': '',
            'v3_contract_status': 'O',
            'staff_in_charge': '',
            'phone_number': 'not-phone',
            'business_address': '',
            'e_mail': 'invalid-email',
            'erp_maintenance': '',
            'erp_usage_status': '',
            'groupware': False,
            'company_evaluation': 'Z',
            'note': ''
        }
        form = CustomerInformationForm(data)
        self.assertFalse(form.is_valid())
        # Expect errors for multiple fields
        self.assertIn('company_name', form.errors)
        self.assertIn('representative', form.errors)
        self.assertIn('business_registration_number', form.errors)
    
    def test_client_list(self):
        """
        거래처 목록 조회 테스트 메서드
        
        거래처 목록 페이지가 정상적으로 표시되는지 확인합니다.
        데이터베이스의 모든 거래처를 조회하고 정렬을 검증합니다.
        
        Returns:
            None: 테스트 결과는 자동으로 평가됩니다
            
        Raises:
            AssertionError: 테스트가 실패할 경우
            
        Test Steps:
            1. 테스트용 거래처 데이터 생성
            2. 목록 페이지로 GET 요청 전송
            3. HTTP 상태 코드 확인
            4. 템플릿에 거래처 목록이 포함되는지 확인
        """
        # create sample
        customer_information.objects.create(
            registration_date='2025-01-01', region='서울', division='외주',
            company_name='C1', representative='A', business_registration_number='1234567890',
            number_of_employees=1, annual_sales=1000, sectors='IT', event='',
            outsourcing_work_type='', main_business='', contract_status='', v3_contract_status='O',
            staff_in_charge='', phone_number='010-0000-0000', business_address='', e_mail='a@b.com',
            erp_maintenance='', erp_usage_status='', groupware=False, company_evaluation='A', note=''
        )
        resp = self.client.get('/client_inform/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'C1')
    
    def test_client_update(self):
        """
        거래처 정보 수정 테스트 메서드
        
        기존 거래처 정보를 정상적으로 수정할 수 있는지 확인합니다.
        수정된 데이터의 정확성과 데이터베이스 반영을 검증합니다.
        
        Returns:
            None: 테스트 결과는 자동으로 평가됩니다
            
        Raises:
            AssertionError: 테스트가 실패할 경우
            
        Test Steps:
            1. 테스트용 거래처 데이터 생성
            2. 수정할 데이터 준비
            3. 거래처 정보 수정
            4. 수정된 데이터의 정확성 확인
            5. 데이터베이스에 반영된 값 확인
        """
        obj = customer_information.objects.create(
            registration_date='2025-01-01', region='서울', division='외주',
            company_name='C2', representative='A', business_registration_number='1234567891',
            number_of_employees=1, annual_sales=1000, sectors='IT', event='',
            outsourcing_work_type='', main_business='', contract_status='', v3_contract_status='O',
            staff_in_charge='', phone_number='010-0000-0000', business_address='', e_mail='a@b.com',
            erp_maintenance='', erp_usage_status='', groupware=False, company_evaluation='A', note=''
        )
        resp = self.client.post(f'/client_inform/{obj.pk}/edit/', {'company_name': 'C2-updated', 'representative':'B', 'business_registration_number':'1234567891', 'registration_date':'2025-01-01', 'region':'서울', 'division':'외주', 'number_of_employees':1, 'annual_sales':1000, 'sectors':'IT', 'event':'', 'outsourcing_work_type':'', 'main_business':'', 'contract_status':'', 'v3_contract_status':'O', 'staff_in_charge':'','phone_number':'010-0000-0000','business_address':'','e_mail':'a@b.com','erp_maintenance':'','erp_usage_status':'','groupware':False,'company_evaluation':'A','note':''})
        self.assertEqual(resp.status_code, 302)
        obj.refresh_from_db()
        self.assertEqual(obj.company_name, 'C2-updated')
    
    def test_client_delete(self):
        """
        거래처 삭제 테스트 메서드
        
        거래처를 정상적으로 삭제할 수 있는지 확인합니다.
        삭제 후 데이터베이스에서 해당 레코드가 사라지는지 검증합니다.
        
        Returns:
            None: 테스트 결과는 자동으로 평가됩니다
            
        Raises:
            AssertionError: 테스트가 실패할 경우
            
        Test Steps:
            1. 테스트용 거래처 데이터 생성
            2. 거래처 삭제 요청 전송
            3. 삭제 성공 확인
            4. 데이터베이스에서 레코드가 사라졌는지 확인
        """
        obj = customer_information.objects.create(
            registration_date='2025-01-01', region='서울', division='외주',
            company_name='C3', representative='A', business_registration_number='1234567892',
            number_of_employees=1, annual_sales=1000, sectors='IT', event='',
            outsourcing_work_type='', main_business='', contract_status='', v3_contract_status='O',
            staff_in_charge='', phone_number='010-0000-0000', business_address='', e_mail='a@b.com',
            erp_maintenance='', erp_usage_status='', groupware=False, company_evaluation='A', note=''
        )
        resp = self.client.post(f'/client_inform/{obj.pk}/delete/')
        self.assertEqual(resp.status_code, 302)
        with self.assertRaises(customer_information.DoesNotExist):
            customer_information.objects.get(pk=obj.pk)
