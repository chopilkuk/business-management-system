from django.test import TestCase

class BusinessStatusTests(TestCase):
    def test_index_page(self):
        """업무 상태 페이지 테스트"""
        response = self.client.get('/businessStatus/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '업무 상태 페이지')
