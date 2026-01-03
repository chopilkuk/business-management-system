"""
유틸리티 모델

이 모듈은 시스템의 유틸리티 데이터 모델을 정의합니다.
보안 이벤트, 사용자 활동 로그 등을 포함합니다.
"""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SecurityEvent(models.Model):
    """보안 이벤트 모델"""
    
    EVENT_TYPES = [
        ('LOGIN_SUCCESS', '로그인 성공'),
        ('LOGIN_FAILED', '로그인 실패'),
        ('LOGOUT', '로그아웃'),
        ('PERMISSION_DENIED', '권한 거부'),
        ('ADMIN_ACCESS_DENIED', '관리자 접근 거부'),
        ('OWNER_ACCESS_DENIED', '소유자 접근 거부'),
        ('CSRF_TOKEN_MISSING', 'CSRF 토큰 누락'),
        ('RATE_LIMIT_EXCEEDED', '속도 제한 초과'),
        ('SUSPICIOUS_ACTIVITY', '의심스러운 활동'),
        ('DATA_ACCESS', '데이터 접근'),
        ('DATA_MODIFICATION', '데이터 수정'),
    ]
    
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, verbose_name='이벤트 타입')
    user = models.CharField(max_length=150, verbose_name='사용자')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='발생 시간')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP 주소')
    user_agent = models.TextField(blank=True, verbose_name='사용자 에이전트')
    details = models.JSONField(default=dict, verbose_name='상세 정보')
    
    class Meta:
        verbose_name = '보안 이벤트'
        verbose_name_plural = '보안 이벤트들'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['event_type', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['ip_address']),
        ]
    
    def __str__(self):
        return f"{self.event_type} - {self.user} ({self.timestamp})"


class ErrorLog(models.Model):
    """오류 로그 모델"""
    error_type = models.CharField(max_length=100)
    error_message = models.TextField()
    traceback = models.TextField()
    context = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=150)
    request_path = models.CharField(max_length=255, null=True, blank=True)
    request_method = models.CharField(max_length=10, null=True, blank=True)
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        verbose_name = '오류 로그'
        verbose_name_plural = '오류 로그들'
        ordering = ['-timestamp']


class UserActivityLog(models.Model):
    """사용자 활동 로그 모델"""
    
    ACTIVITY_TYPES = [
        ('LOGIN', '로그인'),
        ('LOGOUT', '로그아웃'),
        ('DATA_CREATE', '데이터 생성'),
        ('DATA_UPDATE', '데이터 수정'),
        ('DATA_DELETE', '데이터 삭제'),
        ('DATA_VIEW', '데이터 조회'),
        ('FILE_UPLOAD', '파일 업로드'),
        ('FILE_DOWNLOAD', '파일 다운로드'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    details = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    request_path = models.CharField(max_length=255, null=True, blank=True)
    request_method = models.CharField(max_length=10, null=True, blank=True)
    
    class Meta:
        verbose_name = '사용자 활동 로그'
        verbose_name_plural = '사용자 활동 로그들'
        ordering = ['-timestamp']
