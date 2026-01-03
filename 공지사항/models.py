"""
공지사항 앱의 데이터베이스 모델

이 모듈은 시스템 공지사항 관리를 위한 데이터베이스 모델을 정의합니다.
Notice 모델은 공지사항의 모든 정보를 저장하고 관리합니다.

주요 기능:
- 공지사항 기본 정보 저장 (제목, 내용, 작성자)
- 중요도 및 상태 관리
- 조회수 추적
- 작성일 및 수정일 자동 관리
- 작성자 연결 및 권한 관리
"""

# Django의 데이터베이스 모델 관련 기능 임포트
from django.db import models
# Django의 내장 사용자 모델 임포트 (작성자 연결용)
try:
    from django.contrib.auth.models import User
except ImportError:
    User = None
# 최소 길이 검증기 임포트 (제목 최소 길이 검증용)
from django.core.validators import MinLengthValidator
# URL 리버스 기능 임포트 (상세 페이지 URL 생성용)
try:
    from django.urls import reverse
except ImportError:
    reverse = None


class Notice(models.Model):
    """
    공지사항 모델
    
    시스템 공지사항을 관리하는 핵심 데이터 모델입니다.
    작성자, 제목, 내용, 중요도, 상태, 조회수 등을 관리합니다.
    
    Attributes:
        title (Char): 공지사항 제목 (최소 5자, 최대 200자)
        content (TextField): 공지사항 내용 (상세 내용)
        author (ForeignKey): 작성자 (User 모델과 연결)
        importance (Char): 중요도 (낮음, 보통, 높음, 긴급)
        status (Char): 상태 (작성중, 게시됨, 보관됨)
        view_count (PositiveIntegerField): 조회수 (자동 증가)
        created_at (DateTime): 작성일 (자동 설정)
        updated_at (DateTime): 수정일 (자동 업데이트)
        published_at (DateTime): 게시일 (게시 시 자동 설정)
    """
    
    # 중요도 선택지 - 공지사항의 중요도를 정의
    IMPORTANCE_CHOICES = [
        ('low', '낮음'),      # 일반적인 공지사항
        ('medium', '보통'),   # 표준 중요도 공지사항
        ('high', '높음'),     # 중요한 공지사항
        ('urgent', '긴급'),   # 즉시 확인 필요한 긴급 공지사항
    ]
    
    # 상태 선택지 - 공지사항의 현재 상태를 정의
    STATUS_CHOICES = [
        ('draft', '작성중'),     # 아직 게시되지 않은 초안 상태
        ('published', '게시됨'), # 사용자에게 공개된 상태
        ('archived', '보관됨'), # 더 이상 공개되지 않는 보관 상태
    ]
    
    # 제목 필드 - 공지사항의 핵심 제목
    title = models.CharField(
        max_length=200,  # 최대 200자까지 허용
        validators=[MinLengthValidator(5, "제목은 최소 5자 이상이어야 합니다.")],  # 최소 5자 검증
        verbose_name="제목"  # 관리자 사이트 등에서 표시될 필드명
    )
    
    # 내용 필드 - 공지사항의 상세 내용
    content = models.TextField(
        verbose_name="내용",  # 관리자 사이트 등에서 표시될 필드명
        help_text="공지사항 내용을 입력하세요."  # 입력 도움말
    )
    
    # 작성자 필드 - User 모델과 외래키 관계
    author = models.ForeignKey(
        User,  # Django의 내장 User 모델 참조
        on_delete=models.CASCADE,  # 사용자 삭제 시 공지사항도 함께 삭제
        verbose_name="작성자"  # 관리자 사이트 등에서 표시될 필드명
    )
    
    # 중요도 필드 - 공지사항의 중요도 저장
    importance = models.CharField(
        max_length=10,  # 최대 10자
        choices=IMPORTANCE_CHOICES,  # 위에서 정의한 선택지 사용
        default='medium',  # 기본값은 '보통'
        verbose_name="중요도"  # 관리자 사이트 등에서 표시될 필드명
    )
    
    # 상태 필드 - 공지사항의 현재 상태 저장
    status = models.CharField(
        max_length=10,  # 최대 10자
        choices=STATUS_CHOICES,  # 위에서 정의한 선택지 사용
        default='draft',  # 기본값은 '작성중'
        verbose_name="상태"  # 관리자 사이트 등에서 표시될 필드명
    )
    
    # 조회수 필드 - 공지사항 조회 횟수 추적
    view_count = models.PositiveIntegerField(
        default=0,  # 기본값 0
        verbose_name="조회수"  # 관리자 사이트 등에서 표시될 필드명
    )
    
    # 작성일 필드 - 공지사항 최초 작성 시간 (자동 설정)
    created_at = models.DateTimeField(
        auto_now_add=True,  # 객체 생성 시 자동으로 현재 시간 저장
        verbose_name="작성일"  # 관리자 사이트 등에서 표시될 필드명
    )
    
    # 수정일 필드 - 공지사항 수정 시간 (자동 업데이트)
    updated_at = models.DateTimeField(
        auto_now=True,  # 객체 수정 시 자동으로 현재 시간 업데이트
        verbose_name="수정일"  # 관리자 사이트 등에서 표시될 필드명
    )
    
    # 게시일 필드 - 공지사항이 게시된 시간 (수동 설정)
    published_at = models.DateTimeField(
        null=True,  # 필수 필드 아님 (NULL 허용)
        blank=True,  # 폼에서 비워도 됨
        verbose_name="게시일"  # 관리자 사이트 등에서 표시될 필드명
    )

    class Meta:
        """
        모델 메타데이터 클래스
        
        이 클래스는 모델의 동작과 표현을 제어하는 설정을 포함합니다.
        데이터베이스 테이블 이름, 정렬 순서, 제약 조건 등을 정의합니다.
        """
        verbose_name = '공지사항'           # 단수 형태의 모델 이름
        verbose_name_plural = '공지사항들'    # 복수 형태의 모델 이름
        ordering = ['-created_at']      # 기본 정렬 순서 (작성일 최신순)
        
        # 데이터베이스 인덱스 설정 - 검색 성능 향상을 위함
        indexes = [
            models.Index(fields=['status', 'created_at']),  # 상태와 작성일 조합 인덱스
            models.Index(fields=['importance']),              # 중요도 인덱스
            models.Index(fields=['author']),                  # 작성자 인덱스
        ]

    def __str__(self):
        """
        모델 인스턴스의 문자열 표현 메서드
        
        관리자 사이트, 디버깅 등에서 객체를 식별할 때 사용됩니다.
        중요도와 제목을 조합하여 반환합니다.
        
        Returns:
            str: "[중요도] 제목" 형식의 문자열
        """
        return f"[{self.get_importance_display()}] {self.title}"

    def get_absolute_url(self):
        """
        공지사항 상세 페이지 URL 반환 메서드
        
        템플릿에서 공지사항 상세 페이지 링크를 생성할 때 사용됩니다.
        
        Returns:
            str: 공지사항 상세 페이지의 URL
        """
        return reverse('notice_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        """
        모델 저장 메서드
        
        데이터베이스에 모델을 저장하기 전에 추가적인 로직을 수행합니다.
        게시 상태로 변경될 때 게시일을 자동으로 설정합니다.
        
        Args:
            *args: 위치 인자
            **kwargs: 키워드 인자
        """
        # 게시 상태로 변경되고 게시일이 없는 경우 현재 시간으로 설정
        if self.status == 'published' and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)  # 실제 저장 실행

    @property
    def is_published(self):
        """
        게시 여부 확인 프로퍼티
        
        현재 공지사항이 게시된 상태인지 확인합니다.
        
        Returns:
            bool: 게시된 상태이면 True, 아니면 False
        """
        return self.status == 'published'

    @property
    def is_urgent(self):
        """
        긴급 여부 확인 프로퍼티
        
        현재 공지사항이 긴급 중요도인지 확인합니다.
        
        Returns:
            bool: 긴급 중요도이면 True, 아니면 False
        """
        return self.importance == 'urgent'
