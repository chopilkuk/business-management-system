# =============================================================================
# 비즈니스 관리 시스템 기술 관리 앱 관리자 설정
# =============================================================================
# 설명: Django 관리자 사이트에서 기술 관리 모델을 관리하는 설정
# 작성자: 비즈니스 관리 시스템 개발팀
# 버전: 1.0.0
# =============================================================================

# Django 관리자 모듈 임포트
from django.contrib import admin
# 현재 앱의 모델 임포트
from .models import Technology

# =============================================================================
# 관리자 클래스 정의
# =============================================================================
@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    """
    기술 관리 관리자 클래스
    
    Django 관리자 사이트에서 기술 관리 모델을 관리하는 설정을 정의합니다.
    목록 표시, 필터링, 검색, 정렬 등의 기능을 설정합니다.
    
    Attributes:
        list_display (list): 관리자 목록 페이지에 표시할 필드
        list_filter (list): 필터링 옵션을 제공할 필드
        search_fields (list): 검색 기능을 제공할 필드
        ordering (tuple): 기본 정렬 순서
        readonly_fields (tuple): 읽기 전용 필드
        
    Description:
        - 기술 목록의 표시 형식 설정
        - 카테고리별 필터링 기능 제공
        - 이름, 설명 기반 검색 기능 제공
        - 생성일 기준 내림차순 정렬
        - 관리자 사이트의 사용자 경험 최적화
    """
    
    # 관리자 목록 페이지에 표시할 필드 목록
    # 주요 정보를 순서대로 표시하여 정보 파악 용이
    list_display = [
        'name',                 # 기술 이름
        'category',             # 기술 카테고리
        'difficulty_level',      # 난이도 수준
        'status',               # 상태
        'created_at',            # 생성일
        'updated_at',            # 수정일
    ]
    
    # 필터링 옵션을 제공할 필드 목록
    # 다양한 기준으로 기술 필터링 기능 제공
    list_filter = [
        'category',             # 카테고리별 필터링
        'difficulty_level',      # 난이도별 필터링
        'status',                # 상태별 필터링
        'created_at',            # 생성일별 필터링
        'updated_at',            # 수정일별 필터링
    ]
    
    # 검색 기능을 제공할 필드 목록
    # 이름과 설명을 기준으로 검색 기능 제공
    search_fields = [
        'name',                 # 기술 이름 검색
        'description',          # 기술 설명 검색
        'tags',                 # 태그 검색
    ]
    
    # 기본 정렬 순서
    # 생성일 최신순으로 정렬하여 최신 기술 우선 표시
    ordering = ('-created_at',)
    
    # 읽기 전용 필드 목록
    # 일단 생성된 정보는 수정하지 않도록 설정
    readonly_fields = (
        'created_at',            # 생성일시 (수정 불가)
        'updated_at',            # 수정일시 (자동 갱신)
    )
    
    # 목록 페이지에서 페이지당 표시할 레코드 수
    list_per_page = 15
    
    # 상세 페이지 필드셋 설정
    fieldsets = (
        ('기본 정보', {
            'fields': (
                'name',
                'description',
                'category',
                'difficulty_level',
                'status',
            )
        }),
        ('추가 정보', {
            'fields': (
                'tags',
                'documentation_url',
                'examples',
            )
        }),
        ('시간 정보', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)  # 접을 수 있는 섹션
        }),
    )
    
    # 목록 페이지에서 빠른 작업 기능
    actions = ['activate_technologies', 'deactivate_technologies']
    
    def activate_technologies(self, request, queryset):
        """
        선택된 기술을 활성 상태로 변경하는 관리자 액션
        
        Args:
            request: HTTP 요청 객체
            queryset: 선택된 기술 쿼리셋
            
        Returns:
            None: 액션 결과는 메시지로 표시됨
        """
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated}개의 기술이 활성화되었습니다.')
    activate_technologies.short_description = '선택된 기술 활성화'
    
    def deactivate_technologies(self, request, queryset):
        """
        선택된 기술을 비활성 상태로 변경하는 관리자 액션
        
        Args:
            request: HTTP 요청 객체
            queryset: 선택된 기술 쿼리셋
            
        Returns:
            None: 액션 결과는 메시지로 표시됨
        """
        updated = queryset.update(status='inactive')
        self.message_user(request, f'{updated}개의 기술이 비활성화되었습니다.')
    deactivate_technologies.short_description = '선택된 기술 비활성화'
