"""
뷰 테스트 모듈

이 모듈은 모든 뷰의 기능을 테스트합니다.
HTTP 요청/응답, 권한, 템플릿 렌더링 등을 포함합니다.

주요 기능:
- 공지사항 뷰 테스트
- 기술 관리 뷰 테스트
- 거래처 정보 뷰 테스트
- API 뷰 테스트
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
import json

# 모델 임포트
from 공지사항.models import Notice
from 기술.models import Technology
from client_inform.models import customer_information

User = get_user_model()


class NoticeViewTest(TestCase):
    """공지사항 뷰 테스트"""
    
    def setUp(self):
        """테스트 데이터 설정"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.staff_user = User.objects.create_user(
            username='staffuser',
            email='staff@example.com',
            password='staffpass123',
            is_staff=True
        )
        
        self.notice = Notice.objects.create(
            title='테스트 공지사항',
            content='테스트 내용입니다.',
            author=self.user,
            importance='medium',
            status='published'
        )
        
        self.draft_notice = Notice.objects.create(
            title='초안 공지사항',
            content='초안 내용입니다.',
            author=self.user,
            importance='low',
            status='draft'
        )
    
    def test_notice_list_view(self):
        """공지사항 목록 뷰 테스트"""
        # 로그인하지 않은 사용자
        response = self.client.get('/공지사항/')
        self.assertEqual(response.status_code, 302)  # 로그인 페이지로 리다이렉트
        
        # 로그인한 사용자
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/공지사항/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 공지사항')
        self.assertNotContains(response, '초안 공지사항')  # 게시된 공지만 표시
    
    def test_notice_detail_view(self):
        """공지사항 상세 뷰 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(f'/공지사항/{self.notice.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 공지사항')
        self.assertContains(response, '테스트 내용입니다.')
        
        # 조회수 증가 확인
        original_view_count = self.notice.view_count
        response = self.client.get(f'/공지사항/{self.notice.id}/')
        self.notice.refresh_from_db()
        self.assertEqual(self.notice.view_count, original_view_count + 1)
    
    def test_notice_create_view(self):
        """공지사항 생성 뷰 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        # GET 요청
        response = self.client.get('/공지사항/write/')
        self.assertEqual(response.status_code, 200)
        
        # POST 요청
        response = self.client.post('/공지사항/write/', {
            'title': '새 공지사항',
            'content': '새 공지사항 내용',
            'importance': 'high',
            'status': 'draft'
        })
        
        self.assertEqual(response.status_code, 302)  # 성공 시 리다이렉트
        
        # 생성된 공지사항 확인
        new_notice = Notice.objects.get(title='새 공지사항')
        self.assertEqual(new_notice.author, self.user)
        self.assertEqual(new_notice.status, 'draft')
    
    def test_notice_edit_view(self):
        """공지사항 수정 뷰 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        # GET 요청
        response = self.client.get(f'/공지사항/{self.notice.id}/edit/')
        self.assertEqual(response.status_code, 200)
        
        # POST 요청
        response = self.client.post(f'/공지사항/{self.notice.id}/edit/', {
            'title': '수정된 공지사항',
            'content': '수정된 내용',
            'importance': 'high',
            'status': 'published'
        })
        
        self.assertEqual(response.status_code, 302)
        
        # 수정된 공지사항 확인
        self.notice.refresh_from_db()
        self.assertEqual(self.notice.title, '수정된 공지사항')
        self.assertEqual(self.notice.status, 'published')
    
    def test_notice_permission(self):
        """공지사항 권한 테스트"""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        
        self.client.login(username='otheruser', password='otherpass123')
        
        # 다른 사용자의 공지사항 수정 시도
        response = self.client.post(f'/공지사항/{self.notice.id}/edit/', {
            'title': '권한 없는 수정',
            'content': '권한 없는 내용',
            'importance': 'low',
            'status': 'draft'
        })
        
        self.assertEqual(response.status_code, 403)  # 권한 없음
    
    def test_notice_delete_view(self):
        """공지사항 삭제 뷰 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        # GET 요청 (삭제 확인 페이지)
        response = self.client.get(f'/공지사항/{self.notice.id}/delete/')
        self.assertEqual(response.status_code, 200)
        
        # POST 요청 (실제 삭제)
        response = self.client.post(f'/공지사항/{self.notice.id}/delete/')
        self.assertEqual(response.status_code, 302)
        
        # 삭제 확인
        with self.assertRaises(Notice.DoesNotExist):
            Notice.objects.get(id=self.notice.id)
    
    def test_notice_search_and_filter(self):
        """공지사항 검색 및 필터링 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        # 검색
        response = self.client.get('/공지사항/?search=테스트')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 공지사항')
        
        # 중요도 필터
        response = self.client.get('/공지사항/?importance=medium')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 공지사항')
        
        # 상태 필터
        response = self.client.get('/공지사항/?status=published')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 공지사항')


class TechnologyViewTest(TestCase):
    """기술 관리 뷰 테스트"""
    
    def setUp(self):
        """테스트 데이터 설정"""
        self.client = Client()
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
            author=self.user
        )
    
    def test_technology_list_view(self):
        """기술 목록 뷰 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get('/기술/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python')
    
    def test_technology_detail_view(self):
        """기술 상세 뷰 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(f'/기술/{self.technology.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python')
        self.assertContains(response, '프로그래밍 언어')
    
    def test_technology_create_view(self):
        """기술 생성 뷰 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post('/기술/create/', {
            'name': 'JavaScript',
            'category': 'frontend',
            'description': '웹 프로그래밍 언어',
            'proficiency': 'beginner',
            'status': 'learning'
        })
        
        self.assertEqual(response.status_code, 302)
        
        new_tech = Technology.objects.get(name='JavaScript')
        self.assertEqual(new_tech.author, self.user)
        self.assertEqual(new_tech.category, 'frontend')


class ClientInformViewTest(TestCase):
    """거래처 정보 뷰 테스트"""
    
    def setUp(self):
        """테스트 데이터 설정"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.customer = customer_information.objects.create(
            company_name='테스트 회사',
            representative='김대표',
            business_registration_number='123-45-67890',
            sectors='IT',
            contract_status='진행중'
        )
    
    def test_client_list_view(self):
        """거래처 목록 뷰 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get('/client_inform/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 회사')
    
    def test_client_search_view(self):
        """거래처 검색 뷰 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get('/client_inform/', {'search': '테스트'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 회사')


class APIViewTest(TestCase):
    """API 뷰 테스트"""
    
    def setUp(self):
        """테스트 데이터 설정"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.notice = Notice.objects.create(
            title='API 테스트 공지',
            content='API 테스트 내용',
            author=self.user,
            importance='medium',
            status='published'
        )
    
    def test_api_notice_list(self):
        """공지사항 API 목록 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get('/api/v1/notices/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        self.assertIn('pagination', data['data'])
    
    def test_api_notice_detail(self):
        """공지사항 API 상세 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(f'/api/v1/notices/{self.notice.id}/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['title'], 'API 테스트 공지')
    
    def test_api_notice_create(self):
        """공지사항 API 생성 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post('/api/v1/notices/', 
            data=json.dumps({
                'title': 'API 생성 공지',
                'content': 'API 생성 내용',
                'importance': 'high',
                'status': 'draft'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        
        new_notice = Notice.objects.get(title='API 생성 공지')
        self.assertEqual(new_notice.author, self.user)
    
    def test_api_notice_update(self):
        """공지사항 API 수정 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.put(f'/api/v1/notices/{self.notice.id}/',
            data=json.dumps({
                'title': 'API 수정 공지',
                'content': 'API 수정 내용'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        
        self.notice.refresh_from_db()
        self.assertEqual(self.notice.title, 'API 수정 공지')
    
    def test_api_notice_delete(self):
        """공지사항 API 삭제 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.delete(f'/api/v1/notices/{self.notice.id}/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        
        with self.assertRaises(Notice.DoesNotExist):
            Notice.objects.get(id=self.notice.id)
    
    def test_api_search(self):
        """통합 검색 API 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get('/api/v1/search/?q=API')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('results', data['data'])
        
        # 검색 결과 확인
        results = data['data']['results']
        self.assertTrue(any(result['title'] == 'API 테스트 공지' for result in results))
    
    def test_api_stats(self):
        """통계 API 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get('/api/v1/stats/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('notices', data['data'])
        self.assertIn('technologies', data['data'])
        self.assertIn('clients', data['data'])
    
    def test_api_authentication_required(self):
        """API 인증 요구 테스트"""
        # 로그인하지 않은 상태에서 API 호출
        response = self.client.get('/api/v1/notices/')
        self.assertEqual(response.status_code, 302)  # 로그인 페이지로 리다이렉트
    
    def test_api_error_handling(self):
        """API 오류 처리 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        # 존재하지 않는 공지사항 조회
        response = self.client.get('/api/v1/notices/99999/')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['error_code'], 'NOTICE_NOT_FOUND')
        
        # 잘못된 JSON 데이터 전송
        response = self.client.post('/api/v1/notices/',
            data='invalid json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['error_code'], 'INVALID_JSON')


class ViewIntegrationTest(TestCase):
    """뷰 통합 테스트"""
    
    def setUp(self):
        """테스트 데이터 설정"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # 여러 공지사항 생성
        for i in range(5):
            Notice.objects.create(
                title=f'공지사항 {i}',
                content=f'내용 {i}',
                author=self.user,
                importance='medium' if i % 2 == 0 else 'high',
                status='published'
            )
    
    def test_cross_view_consistency(self):
        """뷰 간 일관성 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        # 일반 뷰와 API 뷰의 데이터 일관성 확인
        html_response = self.client.get('/공지사항/')
        api_response = self.client.get('/api/v1/notices/')
        
        self.assertEqual(html_response.status_code, 200)
        self.assertEqual(api_response.status_code, 200)
        
        # API 데이터 확인
        api_data = json.loads(api_response.content)
        notices = api_data['data']['items']
        
        # HTML 페이지에 공지사항이 있는지 확인
        for notice in notices[:3]:  # 처음 3개만 확인
            self.assertContains(html_response, notice['title'])
    
    def test_view_performance(self):
        """뷰 성능 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        import time
        
        # 목록 페이지 성능 측정
        start_time = time.time()
        response = self.client.get('/공지사항/')
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(end_time - start_time, 1.0)  # 1초 이내
        
        # API 성능 측정
        start_time = time.time()
        response = self.client.get('/api/v1/notices/')
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(end_time - start_time, 0.5)  # 0.5초 이내
    
    def test_view_error_handling(self):
        """뷰 오류 처리 테스트"""
        self.client.login(username='testuser', password='testpass123')
        
        # 존재하지 않는 페이지
        response = self.client.get('/공지사항/99999/')
        self.assertEqual(response.status_code, 404)
        
        # 잘못된 HTTP 메서드
        response = self.client.patch('/공지사항/')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed
    
    def test_view_security(self):
        """뷰 보안 테스트"""
        # 로그인하지 않은 상태에서 보호된 페이지 접근
        protected_urls = [
            '/공지사항/write/',
            '/공지사항/1/edit/',
            '/공지사항/1/delete/',
            '/기술/create/',
            '/기술/1/edit/',
        ]
        
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)  # 로그인 페이지로 리다이렉트
