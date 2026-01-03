# =============================================================================
# 비즈니스 관리 시스템 로그인 앱 모델
# =============================================================================
# 설명: 사용자 프로필 정보를 확장하는 데이터 모델 정의
# 작성자: 비즈니스 관리 시스템 개발팀
# 버전: 1.0.0
# =============================================================================

# Django 데이터베이스 모델 임포트
from django.db import models
# Django 기본 사용자 모델 임포트
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    사용자 프로필 확장 모델
    
    Django의 기본 User 모델을 확장하여 추가적인 사용자 정보를 저장
    
    Attributes:
        user (User): Django 기본 사용자 모델과 1:1 관계
        phone (str): 사용자 전화번호 (선택사항)
        department (str): 소속 부서 (선택사항)
        created_at (datetime): 프로필 생성 시간
        
    Methods:
        __str__: 사용자 프로필 문자열 표현
    """
    
    # Django 기본 User 모델과 1:1 관계 설정
    # on_delete=models.CASCADE: 사용자가 삭제되면 프로필도 함께 삭제
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # 전화번호 필드 (선택사항, 최대 20자)
    phone = models.CharField(max_length=20, blank=True)
    
    # 부서 필드 (선택사항, 최대 100자)
    department = models.CharField(max_length=100, blank=True)
    
    # 생성 시간 필드 (자동으로 현재 시간 저장)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        사용자 프로필 문자열 표현 메서드
        
        Returns:
            str: "사용자이름 Profile" 형식의 문자열
        """
        return f"{self.user.username} Profile"
