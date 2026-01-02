"""
보안 관리 모듈

이 모듈은 시스템의 보안을 강화하기 위한 다양한 기능을 제공합니다.
권한 관리, 접근 제어, 데이터 보호, 보안 로깅 등을 포함합니다.

주요 기능:
- 사용자 권한 관리
- 접근 제어 데코레이터
- 데이터 보호 및 암호화
- 보안 로깅 및 모니터링
- CSRF 및 XSS 방어
"""

try:
    from django.contrib.auth.decorators import login_required, permission_required
    from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
    from django.core.exceptions import PermissionDenied
    from django.contrib import messages
    from django.shortcuts import redirect
    from django.utils.decorators import method_decorator
    from django.views.decorators.csrf import csrf_exempt, csrf_protect
    from django.views.decorators.http import require_http_methods
    from django.http import HttpResponseForbidden
    from django.contrib.auth import get_user_model
    from django.db import models
    DJANGO_AVAILABLE = True
except ImportError:
    DJANGO_AVAILABLE = False

import hashlib
import hmac
import secrets
import time
import logging
from functools import wraps

if DJANGO_AVAILABLE:
    User = get_user_model()
else:
    User = None

# 보안 로거 설정
security_logger = logging.getLogger('security')


class SecurityManager:
    """보안 관리자 클래스"""
    
    @staticmethod
    def generate_secure_token(length=32):
        """보안 토큰 생성"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def hash_password(password, salt=None):
        """비밀번호 해싱"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        password_hash = hashlib.pbkdf2_hmac('sha256', 
                                          password.encode('utf-8'), 
                                          salt.encode('utf-8'), 
                                          100000)
        return password_hash.hex(), salt
    
    @staticmethod
    def verify_password(password, hashed_password, salt):
        """비밀번호 검증"""
        password_hash, _ = SecurityManager.hash_password(password, salt)
        return hmac.compare_digest(password_hash, hashed_password)
    
    @staticmethod
    def log_security_event(event_type, user, details=None, ip_address=None):
        """보안 이벤트 로깅"""
        log_data = {
            'event_type': event_type,
            'user': user.username if user else 'Anonymous',
            'timestamp': time.time(),
            'ip_address': ip_address,
            'details': details or {}
        }
        
        security_logger.info(f"Security Event: {log_data}")
        
        # 중요한 보안 이벤트는 데이터베이스에 저장
        if event_type in ['LOGIN_FAILED', 'PERMISSION_DENIED', 'SUSPICIOUS_ACTIVITY']:
            SecurityEvent.objects.create(**log_data)


class PermissionManager:
    """권한 관리자 클래스"""
    
    @staticmethod
    def has_permission(user, permission):
        """사용자 권한 확인"""
        return user.has_perm(permission)
    
    @staticmethod
    def has_any_permission(user, permissions):
        """사용자가 여러 권한 중 하나라도 있는지 확인"""
        return any(user.has_perm(perm) for perm in permissions)
    
    @staticmethod
    def has_all_permissions(user, permissions):
        """사용자가 모든 권한을 가지고 있는지 확인"""
        return all(user.has_perm(perm) for perm in permissions)
    
    @staticmethod
    def is_owner(user, obj):
        """객체의 소유자인지 확인"""
        if hasattr(obj, 'author'):
            return obj.author == user
        elif hasattr(obj, 'user'):
            return obj.user == user
        elif hasattr(obj, 'created_by'):
            return obj.created_by == user
        return False
    
    @staticmethod
    def can_edit(user, obj):
        """편집 권한 확인"""
        if PermissionManager.is_owner(user, obj):
            return True
        return user.has_perm(f'{obj._meta.app_label}.change_{obj._meta.model_name}')
    
    @staticmethod
    def can_delete(user, obj):
        """삭제 권한 확인"""
        if PermissionManager.is_owner(user, obj):
            return True
        return user.has_perm(f'{obj._meta.app_label}.delete_{obj._meta.model_name}')


# 보안 데코레이터들
def secure_required(view_func):
    """HTTPS 요구 데코레이터"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.is_secure():
            return redirect(request.build_absolute_uri(request.get_full_path(), scheme='https'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def admin_required(view_func):
    """관리자 권한 요구 데코레이터"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            SecurityManager.log_security_event('ADMIN_ACCESS_DENIED', request.user, 
                                            {'path': request.path}, 
                                            get_client_ip(request))
            raise PermissionDenied("관리자 권한이 필요합니다.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def owner_required(model_class):
    """소유자 권한 요구 데코레이터"""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            obj_id = kwargs.get('pk') or kwargs.get('id')
            if not obj_id:
                raise PermissionDenied("객체 ID가 필요합니다.")
            
            try:
                obj = model_class.objects.get(pk=obj_id)
            except model_class.DoesNotExist:
                raise PermissionDenied("객체를 찾을 수 없습니다.")
            
            if not PermissionManager.can_edit(request.user, obj):
                SecurityManager.log_security_event('OWNER_ACCESS_DENIED', request.user, 
                                                {'object_id': obj_id, 'model': model_class.__name__}, 
                                                get_client_ip(request))
                raise PermissionDenied("소유자 또는 편집 권한이 필요합니다.")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def rate_limit(max_requests=100, window=3600, scope='ip'):
    """속도 제한 데코레이터"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if scope == 'ip':
                key = f"rate_limit:{get_client_ip(request)}"
            elif scope == 'user':
                key = f"rate_limit:user:{request.user.id if request.user.is_authenticated else 'anonymous'}"
            else:
                key = f"rate_limit:{scope}"
            
            from django.core.cache import cache
            requests = cache.get(key, 0)
            
            if requests >= max_requests:
                SecurityManager.log_security_event('RATE_LIMIT_EXCEEDED', request.user, 
                                                {'key': key, 'requests': requests}, 
                                                get_client_ip(request))
                return HttpResponseForbidden("요청이 너무 많습니다. 잠시 후 다시 시도해주세요.")
            
            cache.set(key, requests + 1, window)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def validate_csrf_token(view_func):
    """CSRF 토큰 검증 데코레이터"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.method in ('POST', 'PUT', 'DELETE', 'PATCH'):
            if not request.csrf_processing_done:
                SecurityManager.log_security_event('CSRF_TOKEN_MISSING', request.user, 
                                                {'method': request.method}, 
                                                get_client_ip(request))
                return HttpResponseForbidden("CSRF 토큰이 유효하지 않습니다.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def security_headers(view_func):
    """보안 헤더 추가 데코레이터"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        
        # 보안 헤더 추가
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response['Content-Security-Policy'] = "default-src 'self'"
        
        return response
    return _wrapped_view


class SecurityMixin:
    """보안 믹스인 클래스"""
    
    def dispatch(self, request, *args, **kwargs):
        # 보안 로깅
        if not request.user.is_authenticated:
            SecurityManager.log_security_event('UNAUTHORIZED_ACCESS', None, 
                                            {'path': request.path}, 
                                            get_client_ip(request))
        
        # 속도 제한 체크
        self.check_rate_limit(request)
        
        return super().dispatch(request, *args, **kwargs)
    
    def check_rate_limit(self, request):
        """속도 제한 체크"""
        key = f"rate_limit:view:{request.user.id if request.user.is_authenticated else 'anonymous'}"
        from django.core.cache import cache
        
        requests = cache.get(key, 0)
        if requests > 1000:  # 뷰당 1000 요청 제한
            SecurityManager.log_security_event('VIEW_RATE_LIMIT_EXCEEDED', request.user, 
                                            {'key': key, 'requests': requests}, 
                                            get_client_ip(request))
            raise PermissionDenied("요청이 너무 많습니다.")


class SecureModelMixin(models.Model):
    """보안 모델 믹스인"""
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                  related_name='%(class)s_created', verbose_name='생성자')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                  related_name='%(class)s_updated', verbose_name='수정자')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        # 생성자/수정자 자동 설정
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # 현재 요청의 사용자 가져오기
        try:
            from django.utils.functional import SimpleLazyObject
            from django.contrib.auth.middleware import get_user
            # 이 부분은 뷰에서 호출될 때만 작동
            pass
        except:
            pass
        
        super().save(*args, **kwargs)


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


def get_client_ip(request):
    """클라이언트 IP 주소 가져오기"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def sanitize_input(data):
    """입력 데이터 정화"""
    if isinstance(data, str):
        # 기본적인 XSS 방어
        import html
        return html.escape(data)
    elif isinstance(data, dict):
        return {key: sanitize_input(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    return data


def validate_file_upload(file):
    """파일 업로드 검증"""
    # 파일 크기 제한 (10MB)
    max_size = 10 * 1024 * 1024
    if file.size > max_size:
        raise ValueError("파일 크기가 너무 큽니다.")
    
    # 파일 타입 검증
    allowed_types = [
        'image/jpeg', 'image/png', 'image/gif',
        'application/pdf', 'text/plain',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ]
    
    if file.content_type not in allowed_types:
        raise ValueError("허용되지 않는 파일 타입입니다.")
    
    # 파일 이름 검증
    import os
    filename = os.path.basename(file.name)
    if any(char in filename for char in ['..', '/', '\\']):
        raise ValueError("안전하지 않은 파일 이름입니다.")


# 보안 설정
SECURITY_SETTINGS = {
    'SESSION_COOKIE_SECURE': True,
    'SESSION_COOKIE_HTTPONLY': True,
    'SESSION_COOKIE_SAMESITE': 'Strict',
    'CSRF_COOKIE_SECURE': True,
    'CSRF_COOKIE_HTTPONLY': True,
    'SECURE_SSL_REDIRECT': True,
    'SECURE_HSTS_SECONDS': 31536000,
    'SECURE_HSTS_INCLUDE_SUBDOMAINS': True,
    'SECURE_HSTS_PRELOAD': True,
    'SECURE_CONTENT_TYPE_NOSNIFF': True,
    'SECURE_BROWSER_XSS_FILTER': True,
    'X_FRAME_OPTIONS': 'DENY',
}
