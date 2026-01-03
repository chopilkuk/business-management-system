# =============================================================================
# 비즈니스 관리 시스템 업무 상태 앱 모델
# =============================================================================
# 설명: 업무 상태 정보를 관리하는 데이터 모델 정의
# 작성자: 비즈니스 관리 시스템 개발팀
# 버전: 1.0.0
# =============================================================================

# Django 데이터베이스 모델 임포트
from django.db import models


class BusinessStatus(models.Model):
    """
    업무 상태 모델
    
    프로젝트나 업무의 현재 상태를 추적하고 관리하는 모델
    
    Attributes:
        name (str): 업무 상태 이름 (예: 진행중, 완료, 보류 등)
        description (str): 업무 상태에 대한 상세 설명 (선택사항)
        created_at (datetime): 업무 상태 생성 시간
        updated_at (datetime): 업무 상태 마지막 수정 시간
        
    Methods:
        __str__: 업무 상태 이름을 문자열로 반환
    """
    
    # 업무 상태 이름 필드 (최대 100자)
    # 예: '진행중', '완료', '보류', '취소', '시작전' 등
    name = models.CharField(max_length=100)
    
    # 업무 상태 설명 필드 (선택사항)
    # 상태에 대한 상세한 설명이나 메모를 저장
    description = models.TextField(blank=True)
    
    # 생성 시간 필드 (자동으로 현재 시간 저장)
    # 레코드가 처음 생성될 때의 시간을 기록
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 수정 시간 필드 (자동으로 현재 시간 저장)
    # 레코드가 수정될 때마다 시간을 갱신
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        업무 상태 문자열 표현 메서드
        
        Returns:
            str: 업무 상태 이름
        """
        return self.name
