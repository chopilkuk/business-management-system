"""
모델 테스트 모듈

이 모듈은 모든 데이터 모델의 기능을 테스트합니다.
데이터 검증, 관계, 메서드 등을 포함합니다.

주요 기능:
- 공지사항 모델 테스트
- 기술 관리 모델 테스트
- 거래처 정보 모델 테스트
- 사용자 모델 테스트
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta

# 모델 임포트
from 공지사항.models import Notice
from 기술.models import Technology
from client_inform.models import customer_information

User = get_user_model()


class NoticeModelTest(TestCase):
    """공지사항 모델 테스트"""
    
    def setUp(self):
        """테스트 데이터 설정"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.notice = Notice.objects.create(
            title='테스트 공지사항',
            content='테스트 내용입니다.',
            author=self.user,
            importance='medium',
            status='draft'
        )
    
    def test_notice_creation(self):
        """공지사항 생성 테스트"""
        self.assertEqual(self.notice.title, '테스트 공지사항')
        self.assertEqual(self.notice.author, self.user)
        self.assertEqual(self.notice.importance, 'medium')
        self.assertEqual(self.notice.status, 'draft')
        self.assertEqual(self.notice.view_count, 0)
    
    def test_notice_str_representation(self):
        """공지사항 문자열 표현 테스트"""
        expected = '[보통] 테스트 공지사항'
        self.assertEqual(str(self.notice), expected)
    
    def test_notice_absolute_url(self):
        """공지사항 URL 테스트"""
        url = self.notice.get_absolute_url()
        self.assertIn(f'/공지사항/{self.notice.id}/', url)
    
    def test_notice_properties(self):
        """공지사항 프로퍼티 테스트"""
        # 게시되지 않은 상태
        self.assertFalse(self.notice.is_published)
        self.assertFalse(self.notice.is_urgent)
        
        # 게시 상태로 변경
        self.notice.status = 'published'
        self.notice.save()
        self.assertTrue(self.notice.is_published)
        
        # 긴급 상태로 변경
        self.notice.importance = 'urgent'
        self.notice.save()
        self.assertTrue(self.notice.is_urgent)
    
    def test_notice_auto_publish(self):
        """공지사항 자동 게시 테스트"""
        self.notice.status = 'published'
        self.notice.save()
        
        self.assertIsNotNone(self.notice.published_at)
        self.assertEqual(self.notice.status, 'published')
    
    def test_notice_validation(self):
        """공지사항 검증 테스트"""
        # 제목이 너무 짧은 경우
        with self.assertRaises(ValidationError):
            notice = Notice(
                title='짧음',
                content='내용',
                author=self.user
            )
            notice.full_clean()
    
    def test_notice_ordering(self):
        """공지사항 정렬 테스트"""
        # 새로운 공지사항 생성
        new_notice = Notice.objects.create(
            title='새 공지사항',
            content='새 내용',
            author=self.user
        )
        
        # 최신순 정렬 확인
        notices = Notice.objects.all()
        self.assertEqual(notices.first(), new_notice)
        self.assertEqual(notices.last(), self.notice)


class TechnologyModelTest(TestCase):
    """기술 관리 모델 테스트"""
    
    def setUp(self):
        """테스트 데이터 설정"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.technology = Technology.objects.create(
            name='Python',
            category='backend',
            description='프로그래밍 언어',
            proficiency='intermediate',
            status='learning',
            author=self.user,
            tags='프로그래밍, 웹, 백엔드'
        )
    
    def test_technology_creation(self):
        """기술 생성 테스트"""
        self.assertEqual(self.technology.name, 'Python')
        self.assertEqual(self.technology.category, 'backend')
        self.assertEqual(self.technology.author, self.user)
        self.assertEqual(self.technology.proficiency, 'intermediate')
        self.assertEqual(self.technology.status, 'learning')
    
    def test_technology_str_representation(self):
        """기술 문자열 표현 테스트"""
        expected = '[백엔드] - Python'
        self.assertEqual(str(self.technology), expected)
    
    def test_technology_properties(self):
        """기술 프로퍼티 테스트"""
        # 태그 리스트
        expected_tags = ['프로그래밍', '웹', '백엔드']
        self.assertEqual(self.technology.tag_list, expected_tags)
        
        # 학습 완료 여부
        self.assertFalse(self.technology.is_completed)
        
        # 숙련도 레벨
        self.assertEqual(self.technology.proficiency_level, 2)
        
        # 상태 변경
        self.technology.status = 'completed'
        self.technology.save()
        self.assertTrue(self.technology.is_completed)
    
    def test_technology_absolute_url(self):
        """기술 URL 테스트"""
        url = self.technology.get_absolute_url()
        self.assertIn(f'/기술/{self.technology.id}/', url)
    
    def test_technology_unique_constraint(self):
        """기술 고유 제약 조건 테스트"""
        # 동일 사용자가 동일 기술명으로 중복 생성 시도
        with self.assertRaises(Exception):  # IntegrityError
            Technology.objects.create(
                name='Python',
                category='frontend',
                author=self.user
            )
        
        # 다른 사용자는 동일 기술명으로 생성 가능
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        
        other_tech = Technology.objects.create(
            name='Python',
            category='frontend',
            author=other_user
        )
        self.assertEqual(other_tech.name, 'Python')
    
    def test_technology_validation(self):
        """기술 검증 테스트"""
        # 기술명이 너무 짧은 경우
        with self.assertRaises(ValidationError):
            tech = Technology(
                name='P',
                author=self.user
            )
            tech.full_clean()


class CustomerInformationModelTest(TestCase):
    """거래처 정보 모델 테스트"""
    
    def setUp(self):
        """테스트 데이터 설정"""
        self.customer = customer_information.objects.create(
            company_name='테스트 회사',
            representative='김대표',
            business_registration_number='123-45-67890',
            sectors='IT',
            number_of_employees=50,
            annual_sales=1000000000,
            contract_status='진행중'
        )
    
    def test_customer_creation(self):
        """거래처 생성 테스트"""
        self.assertEqual(self.customer.company_name, '테스트 회사')
        self.assertEqual(self.customer.representative, '김대표')
        self.assertEqual(self.customer.business_registration_number, '123-45-67890')
        self.assertEqual(self.customer.sectors, 'IT')
        self.assertEqual(self.customer.number_of_employees, 50)
        self.assertEqual(self.customer.annual_sales, 1000000000)
    
    def test_customer_str_representation(self):
        """거래처 문자열 표현 테스트"""
        self.assertEqual(str(self.customer), '테스트 회사')
    
    def test_customer_properties(self):
        """거래처 프로퍼티 테스트"""
        # 완전한 주소
        self.assertEqual(self.customer.get_full_address, '주소 정보 없음')
        
        # 주소 설정 후
        self.customer.business_address = '서울시 강남구'
        self.customer.save()
        self.assertEqual(self.customer.get_full_address, '서울시 강남구')
        
        # 활성 계약 여부
        self.assertTrue(self.customer.is_active_contract)
        
        # V3 계약 여부
        self.assertFalse(self.customer.has_v3_contract)
        
        # V3 계약 상태 변경
        self.customer.v3_contract_status = 'O'
        self.customer.save()
        self.assertTrue(self.customer.has_v3_contract)
    
    def test_customer_display_methods(self):
        """거래처 표시 메서드 테스트"""
        # 종업원수 표시
        self.assertEqual(self.customer.get_employee_count_display, '50명')
        
        # 0명인 경우
        self.customer.number_of_employees = 0
        self.customer.save()
        self.assertEqual(self.customer.get_employee_count_display, '미정보')
        
        # 매출액 표시
        self.assertEqual(self.customer.get_sales_display, '10억원')
        
        # 0원인 경우
        self.customer.annual_sales = 0
        self.customer.save()
        self.assertEqual(self.customer.get_sales_display, '미정보')
    
    def test_customer_validation(self):
        """거래처 검증 테스트"""
        # 사업자등록번호 형식 오류
        with self.assertRaises(ValidationError):
            self.customer.business_registration_number = 'invalid-number'
            self.customer.full_clean()
        
        # 이메일 형식 오류
        with self.assertRaises(ValidationError):
            self.customer.e_mail = 'invalid-email'
            self.customer.full_clean()
        
        # 음수 값 검증
        with self.assertRaises(ValidationError):
            self.customer.number_of_employees = -1
            self.customer.full_clean()
    
    def test_customer_unique_constraint(self):
        """거래처 고유 제약 조건 테스트"""
        # 동일 사업자등록번호로 중복 생성 시도
        with self.assertRaises(Exception):  # IntegrityError
            customer_information.objects.create(
                company_name='다른 회사',
                representative='이대표',
                business_registration_number='123-45-67890'
            )
    
    def test_customer_auto_save(self):
        """거래처 자동 저장 테스트"""
        # 등록일이 없는 경우
        customer = customer_information(
            company_name='자동 테스트 회사',
            representative='자대표',
            business_registration_number='987-65-43210'
        )
        customer.save()
        
        # 등록일이 자동으로 설정되었는지 확인
        self.assertIsNotNone(customer.registration_date)
        
        # 문자열 필드 공백 정리
        customer.company_name = '  자동 테스트 회사  '
        customer.save()
        self.assertEqual(customer.company_name, '자동 테스트 회사')


class UserModelTest(TestCase):
    """사용자 모델 테스트"""
    
    def test_user_creation(self):
        """사용자 생성 테스트"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_user_str_representation(self):
        """사용자 문자열 표현 테스트"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.assertEqual(str(user), 'testuser')
    
    def test_superuser_creation(self):
        """슈퍼유저 생성 테스트"""
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.has_perm('auth.add_user'))
    
    def test_user_permissions(self):
        """사용자 권한 테스트"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # 일반 사용자는 관리자 권한 없음
        self.assertFalse(user.has_perm('admin.add_logentry'))
        
        # 스태프 사용자 생성
        staff_user = User.objects.create_user(
            username='staffuser',
            email='staff@example.com',
            password='staffpass123',
            is_staff=True
        )
        
        # 스태프 사용자는 일부 권한 있음
        self.assertTrue(staff_user.has_perm('admin.add_logentry'))


class ModelIntegrationTest(TestCase):
    """모델 통합 테스트"""
    
    def setUp(self):
        """테스트 데이터 설정"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.notice = Notice.objects.create(
            title='통합 테스트 공지',
            content='통합 테스트 내용',
            author=self.user,
            importance='high',
            status='published'
        )
        
        self.technology = Technology.objects.create(
            name='Django',
            category='backend',
            description='웹 프레임워크',
            proficiency='advanced',
            status='completed',
            author=self.user
        )
    
    def test_cross_model_relationships(self):
        """모델 간 관계 테스트"""
        # 동일 작성자 확인
        self.assertEqual(self.notice.author, self.technology.author)
        
        # 작성자의 공지사항 목록
        user_notices = Notice.objects.filter(author=self.user)
        self.assertIn(self.notice, user_notices)
        
        # 작성자의 기술 목록
        user_technologies = Technology.objects.filter(author=self.user)
        self.assertIn(self.technology, user_technologies)
    
    def test_data_consistency(self):
        """데이터 일관성 테스트"""
        # 공지사항 조회수 증가
        original_view_count = self.notice.view_count
        self.notice.view_count += 1
        self.notice.save()
        
        self.assertEqual(self.notice.view_count, original_view_count + 1)
        
        # 기술 상태 변경
        self.technology.status = 'certified'
        self.technology.save()
        
        self.assertTrue(self.technology.is_completed)
        self.assertEqual(self.technology.status, 'certified')
    
    def test_query_optimization(self):
        """쿼리 최적화 테스트"""
        # select_related 사용
        notice_with_author = Notice.objects.select_related('author').get(id=self.notice.id)
        self.assertEqual(notice_with_author.author.username, 'testuser')
        
        # prefetch_related 사용 (다대다 관계가 있는 경우)
        # 이 테스트는 실제 다대다 관계가 있을 때 추가
        
    def test_bulk_operations(self):
        """대량 작업 테스트"""
        # 대량 공지사항 생성
        notices_data = [
            Notice(
                title=f'대량 테스트 공지 {i}',
                content=f'대량 테스트 내용 {i}',
                author=self.user,
                importance='medium',
                status='draft'
            )
            for i in range(10)
        ]
        
        created_notices = Notice.objects.bulk_create(notices_data)
        self.assertEqual(len(created_notices), 10)
        
        # 대량 업데이트
        Notice.objects.filter(author=self.user).update(status='published')
        
        published_count = Notice.objects.filter(author=self.user, status='published').count()
        self.assertEqual(published_count, 11)  # 기존 1개 + 새로 생성 10개
