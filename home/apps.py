# =============================================================================
# 비즈니스 관리 시스템 홈 앱 설정
# =============================================================================
# 설명: Django 홈 앱의 설정 클래스를 정의
# 작성자: 비즈니스 관리 시스템 개발팀
# 버전: 1.0.0
# =============================================================================

# Django 앱 설정 클래스 임포트
from django.apps import AppConfig


class HomeConfig(AppConfig):
    """
    홈 앱 설정 클래스
    
    Django 앱의 기본 설정을 정의하고 앱의 동작을 제어
    
    Attributes:
        default_auto_field (str): 기본 자동 필드 타입
        name (str): 앱의 이름
        
    Description:
        - 홈 앱의 기본 설정을 관리
        - 데이터베이스 자동 필드 타입 지정
        - 앱의 이름과 메타데이터 정의
    """
    
    # 기본 자동 필드를 BigAutoField로 설정
    # BigAutoField는 큰 숫자 ID를 지원하여 대용량 데이터에 적합
    default_auto_field = 'django.db.models.BigAutoField'
    
    # 앱의 이름을 'home'으로 설정
    # 이 이름은 Django 프로젝트에서 앱을 식별하는 데 사용됨
    name = 'home'
