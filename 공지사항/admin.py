# =============================================================================
# 비즈니스 관리 시스템 공지사항 앱 관리자 설정
# =============================================================================
# 설명: Django 관리자 사이트에서 공지사항 모델을 관리하는 설정
# 작성자: 비즈니스 관리 시스템 개발팀
# 버전: 1.0.0
# =============================================================================

# Django 관리자 모듈 임포트
from django.contrib import admin
# 현재 앱의 모델 임포트
from .models import Notice

# =============================================================================
# 관리자 클래스 정의
# =============================================================================
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    """
    공지사항 관리자 클래스
    
    Django 관리자 사이트에서 공지사항 모델을 관리하는 설정을 정의합니다.
    목록 표시, 필터링, 검색, 정렬 등의 기능을 설정합니다.
    
    Attributes:
        list_display (list): 관리자 목록 페이지에 표시할 필드
        list_filter (list): 필터링 옵션을 제공할 필드
        search_fields (list): 검색 기능을 제공할 필드
        ordering (tuple): 기본 정렬 순서
        readonly_fields (tuple): 읽기 전용 필드
        
    Description:
        - 공지사항 목록의 표시 형식 설정
        - 상태별, 중요도별 필터링 기능 제공
        - 제목, 내용 기반 검색 기능 제공
        - 생성일 기준 내림차순 정렬
        - 관리자 사이트의 사용자 경험 최적화
    """
    
    # 관리자 목록 페이지에 표시할 필드 목록
    # 주요 정보를 순서대로 표시하여 정보 파악 용이
    list_display = [
        'title',                 # 공지사항 제목
        'author',                # 작성자
        'importance',            # 중요도
        'status',                # 상태
        'view_count',            # 조회수
        'created_at',            # 생성일
        'updated_at',            # 수정일
    ]
    
    # 필터링 옵션을 제공할 필드 목록
    # 다양한 기준으로 공지사항 필터링 기능 제공
    list_filter = [
        'status',                # 상태별 필터링 (게시됨, 보관됨 등)
        'importance',            # 중요도별 필터링 (높음, 보통, 낮음)
        'created_at',            # 생성일별 필터링
        'updated_at',            # 수정일별 필터링
        'author',                # 작성자별 필터링
    ]
    
    # 검색 기능을 제공할 필드 목록
    # 제목과 내용을 기준으로 검색 기능 제공
    search_fields = [
        'title',                 # 제목 검색
        'content',               # 내용 검색
        'author__username',      # 작성자 이름 검색
    ]
    
    # 기본 정렬 순서
    # 생성일 최신순으로 정렬하여 최신 공지사항 우선 표시
    ordering = ('-created_at',)
    
    # 읽기 전용 필드 목록
    # 일단 생성된 정보는 수정하지 않도록 설정
    readonly_fields = (
        'view_count',            # 조회수 (자동 증가)
        'created_at',            # 생성일시 (수정 불가)
        'updated_at',            # 수정일시 (자동 갱신)
    )
    
    # 목록 페이지에서 페이지당 표시할 레코드 수
    list_per_page = 20
    
    # 상세 페이지 필드셋 설정
    fieldsets = (
        ('기본 정보', {
            'fields': (
                'title',
                'content',
                'author',
                'importance',
                'status',
            )
        }),
        ('통계 정보', {
            'fields': (
                'view_count',
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)  # 접을 수 있는 섹션
        }),
    )
    
    # 목록 페이지에서 빠른 작업 기능
    actions = ['publish_notices', 'archive_notices']
    
    def publish_notices(self, request, queryset):
        """
        선택된 공지사항을 게시 상태로 변경하는 관리자 액션
        
        Args:
            request: HTTP 요청 객체
            queryset: 선택된 공지사항 쿼리셋
            
        Returns:
            None: 액션 결과는 메시지로 표시됨
        """
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated}개의 공지사항이 게시되었습니다.')
    publish_notices.short_description = '선택된 공지사항 게시'
    
    def archive_notices(self, request, queryset):
        """
        선택된 공지사항을 보관 상태로 변경하는 관리자 액션
        
        Args:
            request: HTTP 요청 객체
            queryset: 선택된 공지사항 쿼리셋
            
        Returns:
            None: 액션 결과는 메시지로 표시됨
        """
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated}개의 공지사항이 보관되었습니다.')
    archive_notices.short_description = '선택된 공지사항 보관'
