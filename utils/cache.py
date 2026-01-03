"""
캐싱 관리 모듈

이 모듈은 데이터베이스 쿼리 성능 최적화를 위한 캐싱 기능을 제공합니다.
메모리 캐시, 데이터베이스 쿼리 캐시, 템플릿 캐시 등을 관리합니다.

주요 기능:
- 메모리 캐시 설정
- 데이터베이스 쿼리 최적화
- 캐시 무효화 및 관리
- 성능 모니터링
"""

try:
    from django.core.cache import cache
    from django.db import models
    from django.core.cache.utils import make_template_fragment_key
    from django.template import loader
    from django.utils.decorators import method_decorator
    from django.views.decorators.cache import cache_page
    from django.views.decorators.vary import vary_on_headers, vary_on_cookie
    DJANGO_AVAILABLE = True
except ImportError:
    DJANGO_AVAILABLE = False

import time
import functools


class CacheManager:
    """캐시 관리자 클래스"""
    
    @staticmethod
    def get_cache_key(key_prefix, *args, **kwargs):
        """캐시 키 생성"""
        key_parts = [key_prefix]
        key_parts.extend(str(arg) for arg in args)
        key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
        return ':'.join(key_parts)
    
    @staticmethod
    def cache_result(key_prefix, timeout=300):
        """함수 결과 캐싱 데코레이터"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = CacheManager.get_cache_key(key_prefix, *args, **kwargs)
                result = cache.get(cache_key)
                
                if result is not None:
                    return result
                
                result = func(*args, **kwargs)
                cache.set(cache_key, result, timeout)
                return result
            
            return wrapper
        return decorator
    
    @staticmethod
    def invalidate_cache(key_prefix, *args, **kwargs):
        """특정 캐시 무효화"""
        cache_key = CacheManager.get_cache_key(key_prefix, *args, **kwargs)
        cache.delete(cache_key)
    
    @staticmethod
    def invalidate_pattern(pattern):
        """패턴에 해당하는 캐시 무효화"""
        # Django의 캐시 백엔드에서 패턴 일치 키 삭제
        # 실제 구현에서는 Redis와 같은 캐시 백엔드 사용 권장
        try:
            from django.core.cache import caches
            # Redis의 경우: caches['default'].delete_pattern(pattern)
            # 여기서는 간단화된 구현
            cache.clear()  # 모든 캐시 초기화 (개발 환경에서는 충분)
        except Exception as e:
            print(f"캐시 무효화 오류: {e}")


class QueryOptimizer:
    """데이터베이스 쿼리 최적화 클래스"""
    
    @staticmethod
    def optimize_queryset(queryset, select_related=None, prefetch_related=None):
        """쿼리셋 최적화"""
        if select_related:
            queryset = queryset.select_related(*select_related)
        
        if prefetch_related:
            queryset = queryset.prefetch_related(*prefetch_related)
        
        return queryset
    
    @staticmethod
    def bulk_create_with_cache(model_class, objects, cache_key_prefix=None, timeout=300):
        """대량 생성 및 캐싱"""
        created_objects = model_class.objects.bulk_create(objects)
        
        if cache_key_prefix:
            cache_key = CacheManager.get_cache_key(cache_key_prefix, 'bulk_create')
            cache.set(cache_key, created_objects, timeout)
        
        return created_objects
    
    @staticmethod
    def get_or_create_cached(model_class, defaults=None, **kwargs):
        """get_or_create 캐싱 버전"""
        cache_key = CacheManager.get_cache_key('get_or_create', model_class.__name__, **kwargs)
        
        try:
            obj = cache.get(cache_key)
            if obj is not None:
                return obj, False
            
            obj, created = model_class.objects.get_or_create(defaults=defaults, **kwargs)
            cache.set(cache_key, obj, 300)
            return obj, created
        except model_class.DoesNotExist:
            obj, created = model_class.objects.get_or_create(defaults=defaults, **kwargs)
            cache.set(cache_key, obj, 300)
            return obj, created


class TemplateCache:
    """템플릿 캐시 관리 클래스"""
    
    @staticmethod
    def get_cached_template(template_name, timeout=300):
        """캐시된 템플릿 가져오기"""
        cache_key = make_template_fragment_key(template_name)
        template = cache.get(cache_key)
        
        if template is None:
            template = loader.get_template(template_name)
            cache.set(cache_key, template, timeout)
        
        return template
    
    @staticmethod
    def render_cached_template(template_name, context, timeout=300):
        """캐시된 템플릿 렌더링"""
        cache_key = CacheManager.get_cache_key('template_render', template_name, str(context))
        cached_content = cache.get(cache_key)
        
        if cached_content is not None:
            return cached_content
        
        template = TemplateCache.get_cached_template(template_name, timeout)
        content = template.render(context)
        cache.set(cache_key, content, timeout)
        
        return content


class PerformanceMonitor:
    """성능 모니터링 클래스"""
    
    @staticmethod
    def monitor_query_performance(func):
        """쿼리 성능 모니터링 데코레이터"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.time()
                duration = end_time - start_time
                
                # 성능 기록 (실제로는 로그 파일이나 데이터베이스에 저장)
                if duration > 1.0:  # 1초 이상 걸리는 쿼리만 기록
                    print(f"느린 쿼리 감지: {func.__name__} - {duration:.2f}초")
                
                # 성능 통계 수집
                PerformanceMonitor.record_performance_stats(func.__name__, duration)
        
        return wrapper
    
    @staticmethod
    def record_performance_stats(query_name, duration):
        """성능 통계 기록"""
        stats = cache.get('performance_stats', {})
        
        if query_name not in stats:
            stats[query_name] = {
                'count': 0,
                'total_time': 0,
                'avg_time': 0,
                'max_time': 0,
                'min_time': float('inf')
            }
        
        stats[query_name]['count'] += 1
        stats[query_name]['total_time'] += duration
        stats[query_name]['avg_time'] = stats[query_name]['total_time'] / stats[query_name]['count']
        stats[query_name]['max_time'] = max(stats[query_name]['max_time'], duration)
        stats[query_name]['min_time'] = min(stats[query_name]['min_time'], duration)
        
        cache.set('performance_stats', stats, 3600)  # 1시간 동안 캐시


# 캐싱 데코레이터들
def cache_view(timeout=300):
    """뷰 캐싱 데코레이터"""
    return cache_page(timeout)(lambda view: view)

def cache_fragment(timeout=300):
    """템플릿 프래그먼트 캐싱 데코레이터"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = CacheManager.get_cache_key('fragment', func.__name__, *args, **kwargs)
            result = cache.get(cache_key)
            
            if result is not None:
                return result
            
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result
        
        return wrapper
    return decorator

def vary_on_user_agent(timeout=300):
    """User-Agent에 따른 캐싱"""
    return vary_on_headers('User-Agent')(cache_page(timeout))

def vary_on_user(timeout=300):
    """사용자에 따른 캐싱"""
    return vary_on_cookie(cache_page(timeout))


# 자주 사용되는 캐싱 설정
CACHE_SETTINGS = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
            'CULL_FREQUENCY': 3,
        }
    },
    'sessions': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
        'TIMEOUT': 3600,
    },
    'template_fragments': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 300,
    },
}

# 캐시 키 접두사들
CACHE_KEY_PREFIXES = {
    'notice': 'notice',
    'technology': 'tech',
    'client': 'client',
    'user': 'user',
    'search': 'search',
    'stats': 'stats',
}

# 캐시 시간 설정 (초 단위)
CACHE_TIMEOUTS = {
    'short': 60,      # 1분
    'medium': 300,    # 5분
    'long': 900,      # 15분
    'very_long': 3600, # 1시간
}
