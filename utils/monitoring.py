"""
모니터링 및 로깅 시스템

이 모듈은 시스템의 모든 활동을 모니터링하고 로깅하는 기능을 제공합니다.
성능 모니터링, 오류 추적, 사용자 활동 추적 등을 포함합니다.

주요 기능:
- 시스템 성능 모니터링
- 오류 로깅 및 추적
- 사용자 활동 모니터링
- 데이터베이스 쿼리 모니터맅
- 시스템 리소스 모니터링
"""

import logging
import time
import json
from datetime import datetime, timedelta
from functools import wraps
import traceback
import threading

try:
    import psutil
except ImportError:
    psutil = None

try:
    from django.conf import settings
    from django.core.cache import cache
    from django.db import connection
    from django.contrib.auth import get_user_model
    from django.http import HttpRequest
    User = get_user_model()
    DJANGO_AVAILABLE = True
except ImportError:
    DJANGO_AVAILABLE = False
    User = None

# 로거 설정
system_logger = logging.getLogger('system')
performance_logger = logging.getLogger('performance')
error_logger = logging.getLogger('error')
user_activity_logger = logging.getLogger('user_activity')


class SystemMonitor:
    """시스템 모니터링 클래스"""
    
    @staticmethod
    def get_system_stats():
        """시스템 통계 정보 가져오기"""
        try:
            stats = {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent,
                'network_io': {
                    'bytes_sent': psutil.net_io_counters().bytes_sent,
                    'bytes_recv': psutil.net_io_counters().bytes_recv,
                },
                'process_count': len(psutil.pids()),
                'timestamp': datetime.now().isoformat()
            }
            return stats
        except Exception as e:
            error_logger.error(f"시스템 통계 수집 오류: {str(e)}")
            return None
    
    @staticmethod
    def get_database_stats():
        """데이터베이스 통계 정보 가져오기"""
        try:
            with connection.cursor() as cursor:
                # 데이터베이스 크기 (SQLite)
                cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
                db_size = cursor.fetchone()[0] if cursor.fetchone() else 0
                
                # 테이블 통계
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                
                table_stats = {}
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    table_stats[table_name] = count
                
                stats = {
                    'database_size': db_size,
                    'table_stats': table_stats,
                    'connection_count': len(connection.connections),
                    'timestamp': datetime.now().isoformat()
                }
                
                return stats
        except Exception as e:
            error_logger.error(f"데이터베이스 통계 수집 오류: {str(e)}")
            return None
    
    @staticmethod
    def get_cache_stats():
        """캐시 통계 정보 가져오기"""
        try:
            # 기본 캐시 정보
            cache_info = {
                'backend': settings.CACHES['default']['BACKEND'],
                'timeout': settings.CACHES['default'].get('TIMEOUT', 300),
                'timestamp': datetime.now().isoformat()
            }
            
            # 캐시 키 개수 (LocMemCache의 경우)
            if hasattr(cache, '_cache'):
                cache_info['key_count'] = len(cache._cache)
            
            return cache_info
        except Exception as e:
            error_logger.error(f"캐시 통계 수집 오류: {str(e)}")
            return None


class PerformanceMonitor:
    """성능 모니터링 클래스"""
    
    @staticmethod
    def monitor_performance(func):
        """성능 모니터링 데코레이터"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.time()
                end_memory = psutil.Process().memory_info().rss
                
                duration = end_time - start_time
                memory_diff = end_memory - start_memory
                
                # 성능 데이터 기록
                performance_data = {
                    'function': func.__name__,
                    'duration': duration,
                    'memory_usage': memory_diff,
                    'timestamp': datetime.now().isoformat(),
                    'args_count': len(args),
                    'kwargs_count': len(kwargs)
                }
                
                # 느린 함수 기록
                if duration > 1.0:
                    performance_logger.warning(f"느린 함수: {func.__name__} - {duration:.2f}초")
                
                # 메모리 사용량 많은 함수 기록
                if memory_diff > 10 * 1024 * 1024:  # 10MB 이상
                    performance_logger.warning(f"메모리 사용량 많은 함수: {func.__name__} - {memory_diff / 1024 / 1024:.2f}MB")
                
                # 성능 통계 저장
                PerformanceMonitor.save_performance_stats(performance_data)
            
            return wrapper
        return wrapper
    
    @staticmethod
    def save_performance_stats(data):
        """성능 통계 저장"""
        try:
            stats = cache.get('performance_stats', {})
            
            function_name = data['function']
            if function_name not in stats:
                stats[function_name] = {
                    'count': 0,
                    'total_duration': 0,
                    'avg_duration': 0,
                    'max_duration': 0,
                    'min_duration': float('inf'),
                    'total_memory': 0,
                    'avg_memory': 0,
                    'max_memory': 0,
                    'min_memory': float('inf')
                }
            
            stats[function_name]['count'] += 1
            stats[function_name]['total_duration'] += data['duration']
            stats[function_name]['avg_duration'] = stats[function_name]['total_duration'] / stats[function_name]['count']
            stats[function_name]['max_duration'] = max(stats[function_name]['max_duration'], data['duration'])
            stats[function_name]['min_duration'] = min(stats[function_name]['min_duration'], data['duration'])
            
            stats[function_name]['total_memory'] += data['memory_usage']
            stats[function_name]['avg_memory'] = stats[function_name]['total_memory'] / stats[function_name]['count']
            stats[function_name]['max_memory'] = max(stats[function_name]['max_memory'], data['memory_usage'])
            stats[function_name]['min_memory'] = min(stats[function_name]['min_memory'], data['memory_usage'])
            
            cache.set('performance_stats', stats, 3600)  # 1시간 동안 캐시
            
        except Exception as e:
            error_logger.error(f"성능 통계 저장 오류: {str(e)}")
    
    @staticmethod
    def get_performance_report():
        """성능 보고서 생성"""
        try:
            stats = cache.get('performance_stats', {})
            
            report = {
                'timestamp': datetime.now().isoformat(),
                'functions': {},
                'summary': {
                    'total_functions': len(stats),
                    'slow_functions': [],
                    'memory_intensive_functions': []
                }
            }
            
            for func_name, func_stats in stats.items():
                report['functions'][func_name] = func_stats
                
                # 느린 함수 식별
                if func_stats['avg_duration'] > 1.0:
                    report['summary']['slow_functions'].append({
                        'function': func_name,
                        'avg_duration': func_stats['avg_duration']
                    })
                
                # 메모리 사용량 많은 함수 식별
                if func_stats['avg_memory'] > 10 * 1024 * 1024:  # 10MB
                    report['summary']['memory_intensive_functions'].append({
                        'function': func_name,
                        'avg_memory': func_stats['avg_memory']
                    })
            
            return report
            
        except Exception as e:
            error_logger.error(f"성능 보고서 생성 오류: {str(e)}")
            return None


class ErrorMonitor:
    """오류 모니터링 클래스"""
    
    @staticmethod
    def log_error(error, context=None, user=None, request=None):
        """오류 로깅"""
        try:
            error_data = {
                'error_type': type(error).__name__,
                'error_message': str(error),
                'traceback': traceback.format_exc(),
                'context': context or {},
                'timestamp': datetime.now().isoformat(),
                'user': user.username if user else 'Anonymous',
                'request_path': request.path if request else None,
                'request_method': request.method if request else None,
                'user_agent': request.META.get('HTTP_USER_AGENT') if request else None,
                'ip_address': ErrorMonitor.get_client_ip(request) if request else None
            }
            
            # 오류 로그 기록
            error_logger.error(f"오류 발생: {error_data}")
            
            # 심각한 오류는 데이터베이스에 저장
            if isinstance(error, (Exception,)):
                ErrorMonitor.save_error_to_db(error_data)
            
        except Exception as e:
            error_logger.error(f"오류 로깅 중 오류 발생: {str(e)}")
    
    @staticmethod
    def save_error_to_db(error_data):
        """오류를 데이터베이스에 저장"""
        try:
            from .models import ErrorLog
            ErrorLog.objects.create(**error_data)
        except Exception as e:
            error_logger.error(f"오류 데이터베이스 저장 오류: {str(e)}")
    
    @staticmethod
    def get_client_ip(request):
        """클라이언트 IP 주소 가져오기"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @staticmethod
    def get_error_stats(days=7):
        """오류 통계 가져오기"""
        try:
            from .models import ErrorLog
            from django.utils import timezone
            
            start_date = timezone.now() - timedelta(days=days)
            
            stats = {
                'total_errors': ErrorLog.objects.filter(timestamp__gte=start_date).count(),
                'by_type': {},
                'by_user': {},
                'by_path': {},
                'recent_errors': ErrorLog.objects.filter(
                    timestamp__gte=start_date
                ).order_by('-timestamp')[:10]
            }
            
            # 오류 타입별 통계
            error_types = ErrorLog.objects.filter(timestamp__gte=start_date).values('error_type').distinct()
            for error_type in error_types:
                count = ErrorLog.objects.filter(
                    timestamp__gte=start_date,
                    error_type=error_type['error_type']
                ).count()
                stats['by_type'][error_type['error_type']] = count
            
            # 사용자별 오류 통계
            users = ErrorLog.objects.filter(timestamp__gte=start_date).values('user').distinct()
            for user in users:
                count = ErrorLog.objects.filter(
                    timestamp__gte=start_date,
                    user=user['user']
                ).count()
                stats['by_user'][user['user']] = count
            
            # 경로별 오류 통계
            paths = ErrorLog.objects.filter(timestamp__gte=start_date).values('request_path').distinct()
            for path in paths:
                count = ErrorLog.objects.filter(
                    timestamp__gte=start_date,
                    request_path=path['request_path']
                ).count()
                stats['by_path'][path['request_path']] = count
            
            return stats
            
        except Exception as e:
            error_logger.error(f"오류 통계 수집 오류: {str(e)}")
            return None


class UserActivityMonitor:
    """사용자 활동 모니터링 클래스"""
    
    @staticmethod
    def log_activity(user, activity_type, details=None, request=None):
        """사용자 활동 로깅"""
        try:
            activity_data = {
                'user': user,
                'activity_type': activity_type,
                'details': details or {},
                'timestamp': datetime.now(),
                'ip_address': UserActivityMonitor.get_client_ip(request) if request else None,
                'user_agent': request.META.get('HTTP_USER_AGENT') if request else None,
                'request_path': request.path if request else None,
                'request_method': request.method if request else None
            }
            
            # 활동 로그 기록
            user_activity_logger.info(f"사용자 활동: {activity_data}")
            
            # 중요 활동은 데이터베이스에 저장
            if activity_type in ['LOGIN', 'LOGOUT', 'DATA_CREATE', 'DATA_UPDATE', 'DATA_DELETE']:
                UserActivityMonitor.save_activity_to_db(activity_data)
                
        except Exception as e:
            error_logger.error(f"사용자 활동 로깅 오류: {str(e)}")
    
    @staticmethod
    def save_activity_to_db(activity_data):
        """사용자 활동을 데이터베이스에 저장"""
        try:
            from .models import UserActivityLog
            UserActivityLog.objects.create(**activity_data)
        except Exception as e:
            error_logger.error(f"사용자 활동 데이터베이스 저장 오류: {str(e)}")
    
    @staticmethod
    def get_client_ip(request):
        """클라이언트 IP 주소 가져오기"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @staticmethod
    def get_activity_stats(days=7):
        """사용자 활동 통계 가져오기"""
        try:
            from .models import UserActivityLog
            from django.utils import timezone
            
            start_date = timezone.now() - timedelta(days=days)
            
            stats = {
                'total_activities': UserActivityLog.objects.filter(timestamp__gte=start_date).count(),
                'by_type': {},
                'by_user': {},
                'by_hour': {},
                'recent_activities': UserActivityLog.objects.filter(
                    timestamp__gte=start_date
                ).order_by('-timestamp')[:20]
            }
            
            # 활동 타입별 통계
            activity_types = UserActivityLog.objects.filter(timestamp__gte=start_date).values('activity_type').distinct()
            for activity_type in activity_types:
                count = UserActivityLog.objects.filter(
                    timestamp__gte=start_date,
                    activity_type=activity_type['activity_type']
                ).count()
                stats['by_type'][activity_type['activity_type']] = count
            
            # 사용자별 활동 통계
            users = UserActivityLog.objects.filter(timestamp__gte=start_date).values('user').distinct()
            for user in users:
                count = UserActivityLog.objects.filter(
                    timestamp__gte=start_date,
                    user=user['user']
                ).count()
                stats['by_user'][user['user']] = count
            
            # 시간별 활동 통계
            for hour in range(24):
                count = UserActivityLog.objects.filter(
                    timestamp__gte=start_date,
                    timestamp__hour=hour
                ).count()
                stats['by_hour'][f"{hour:02d}:00"] = count
            
            return stats
            
        except Exception as e:
            error_logger.error(f"사용자 활동 통계 수집 오류: {str(e)}")
            return None


class HealthCheck:
    """시스템 헬스체크 클래스"""
    
    @staticmethod
    def check_database():
        """데이터베이스 헬스체크"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return {'status': 'healthy', 'message': '데이터베이스 연결 정상'}
        except Exception as e:
            return {'status': 'unhealthy', 'message': f'데이터베이스 연결 오류: {str(e)}'}
    
    @staticmethod
    def check_cache():
        """캐시 헬스체크"""
        try:
            test_key = 'health_check_test'
            cache.set(test_key, 'test_value', 10)
            value = cache.get(test_key)
            cache.delete(test_key)
            
            if value == 'test_value':
                return {'status': 'healthy', 'message': '캐시 정상 작동'}
            else:
                return {'status': 'unhealthy', 'message': '캐시 작동 오류'}
        except Exception as e:
            return {'status': 'unhealthy', 'message': f'캐시 오류: {str(e)}'}
    
    @staticmethod
    def check_system_resources():
        """시스템 리소스 헬스체크"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent
            
            status = 'healthy'
            message = '시스템 리소스 정상'
            
            if cpu_percent > 90:
                status = 'warning'
                message = f'CPU 사용량 높음: {cpu_percent}%'
            
            if memory_percent > 90:
                status = 'warning'
                message = f'메모리 사용량 높음: {memory_percent}%'
            
            if disk_percent > 90:
                status = 'warning'
                message = f'디스크 사용량 높음: {disk_percent}%'
            
            return {
                'status': status,
                'message': message,
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'disk_percent': disk_percent
            }
        except Exception as e:
            return {'status': 'unhealthy', 'message': f'시스템 리소스 체크 오류: {str(e)}'}
    
    @staticmethod
    def full_health_check():
        """전체 헬스체크"""
        checks = {
            'database': HealthCheck.check_database(),
            'cache': HealthCheck.check_cache(),
            'system_resources': HealthCheck.check_system_resources(),
            'timestamp': datetime.now().isoformat()
        }
        
        # 전체 상태 계산
        overall_status = 'healthy'
        for check_name, check_result in checks.items():
            if check_name != 'timestamp' and check_result['status'] == 'unhealthy':
                overall_status = 'unhealthy'
                break
            elif check_name != 'timestamp' and check_result['status'] == 'warning':
                overall_status = 'warning'
        
        checks['overall_status'] = overall_status
        
        return checks


# 미들웨어 클래스
class MonitoringMiddleware:
    """모니터링 미들웨어"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = time.time()
        
        # 요청 처리
        response = self.get_response(request)
        
        # 응답 시간 측정
        end_time = time.time()
        duration = end_time - start_time
        
        # 느린 요청 로깅
        if duration > 2.0:
            performance_logger.warning(
                f"느린 요청: {request.method} {request.path} - {duration:.2f}초"
            )
        
        # 요청 통계 저장
        self.save_request_stats(request, duration)
        
        return response
    
    def save_request_stats(self, request, duration):
        """요청 통계 저장"""
        try:
            stats = cache.get('request_stats', {})
            
            path = request.path
            method = request.method
            
            key = f"{method} {path}"
            if key not in stats:
                stats[key] = {
                    'count': 0,
                    'total_duration': 0,
                    'avg_duration': 0,
                    'max_duration': 0,
                    'min_duration': float('inf')
                }
            
            stats[key]['count'] += 1
            stats[key]['total_duration'] += duration
            stats[key]['avg_duration'] = stats[key]['total_duration'] / stats[key]['count']
            stats[key]['max_duration'] = max(stats[key]['max_duration'], duration)
            stats[key]['min_duration'] = min(stats[key]['min_duration'], duration)
            
            cache.set('request_stats', stats, 3600)  # 1시간 동안 캐시
            
        except Exception as e:
            error_logger.error(f"요청 통계 저장 오류: {str(e)}")


# 모델 정의 (utils/models.py에 추가해야 함)
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
