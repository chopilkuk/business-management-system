"""
기술 관리 앱의 데이터베이스 모델

이 모듈은 기술 스택, 프레임워크, 도구 등을 관리하는 데이터베이스 모델을 정의합니다.
Technology 모델은 기술 정보, 분류, 숙련도, 학습 상태 등을 관리합니다.

주요 기능:
- 기술 기본 정보 저장 (이름, 설명, 분류)
- 숙련도 및 학습 상태 관리
- 기술 등록자 및 학습 자료 관리
- 태그 및 메타데이터 관리
- 자동화된 데이터 검증 및 처리
"""

# Django의 데이터베이스 모델 관련 기능 임포트
from django.db import models
# Django의 내장 사용자 모델 임포트 (등록자 연결용)
from django.contrib.auth.models import User
# 최소 길이 검증기 임포트 (기술명 최소 길이 검증용)
from django.core.validators import MinLengthValidator
# URL 리버스 기능 임포트 (상세 페이지 URL 생성용)
from django.urls import reverse


class Technology(models.Model):
    """
    기술 관리 모델
    
    기술 스택, 프레임워크, 도구 등을 관리하는 핵심 데이터 모델입니다.
    기술 분류, 숙련도, 학습 상태, 등록자 정보 등을 관리합니다.
    
    Attributes:
        name (Char): 기술명 (최소 2자, 최대 100자)
        category (Char): 기술 분류 (프론트엔드, 백엔드 등)
        description (TextField): 기술 상세 설명
        proficiency (Char): 숙련도 (초급, 중급, 고급, 전문가)
        status (Char): 학습 상태 (학습중, 학습완료, 자격증보유, 보관됨)
        author (ForeignKey): 등록자 (User 모델과 연결)
        official_document (URLField): 공식 문서 URL
        learning_resources (TextField): 학습 자료
        tags (Char): 검색용 태그
        created_at (DateTime): 생성일 (자동 설정)
        updated_at (DateTime): 수정일 (자동 업데이트)
    """
    
    # 기술 분류 선택지 - 기술의 카테고리를 정의
    CATEGORY_CHOICES = [
        ('frontend', '프론트엔드'),  # 웹 프론트엔드 기술
        ('backend', '백엔드'),      # 서버 사이드 기술
        ('database', '데이터베이스'),  # 데이터베이스 관련 기술
        ('devops', '데브옵스'),        # 개발 운영 기술
        ('mobile', '모바일'),          # 모바일 앱 개발 기술
        ('ai', '인공지능'),           # 인공지능/머신러닝 기술
        ('etc', '기타'),              # 기타 분류 기술
    ]
    
    # 숙련도 선택지 - 기술 숙련도 수준을 정의
    PROFICIENCY_CHOICES = [
        ('beginner', '초급'),       # 기초 수준 (입문자)
        ('intermediate', '중급'),    # 중간 수준 (경험자)
        ('advanced', '고급'),         # 고급 수준 (숙련자)
        ('expert', '전문가'),         # 전문가 수준 (전문가)
    ]
    
    # 상태 선택지 - 기술 학습 상태를 정의
    STATUS_CHOICES = [
        ('learning', '학습중'),       # 현재 학습 중인 상태
        ('completed', '학습완료'),    # 학습을 완료한 상태
        ('certified', '자격증보유'), # 관련 자격증 보유 상태
        ('archived', '보관됨'),        # 더 이상 사용하지 않는 보관 상태
    ]
    
    # 기술명 필드 - 기술의 핵심 식별자
    name = models.CharField(
        max_length=100,  # 최대 100자까지 허용
        validators=[MinLengthValidator(2, "기술명은 최소 2자 이상이어야 합니다.")],  # 최소 2자 검증
        verbose_name="기술명"  # 관리자 사이트 등에서 표시될 필드명
    )
    
    # 분류 필드 - 기술의 카테고리 저장
    category = models.CharField(
        max_length=20,  # 최대 20자
        choices=CATEGORY_CHOICES,  # 위에서 정의한 선택지 사용
        default='etc',  # 기본값은 '기타'
        verbose_name="분류"  # 관리자 사이트 등에서 표시될 필드명
    )
    
    # 설명 필드 - 기술에 대한 상세 설명
    description = models.TextField(
        blank=True,  # 필수 필드 아님 (비워도 됨)
        verbose_name="설명",  # 관리자 사이트 등에서 표시될 필드명
        help_text="기술에 대한 상세 설명을 입력하세요."  # 입력 도움말
    )
    
    # 숙련도 필드 - 현재 숙련도 수준 저장
    proficiency = models.CharField(
        max_length=20,  # 최대 20자
        choices=PROFICIENCY_CHOICES,  # 위에서 정의한 선택지 사용
        default='beginner',  # 기본값은 '초급'
        verbose_name="숙련도"  # 관리자 사이트 등에서 표시될 필드명
    )
    
    # 상태 필드 - 현재 학습 상태 저장
    status = models.CharField(
        max_length=20,  # 최대 20자
        choices=STATUS_CHOICES,  # 위에서 정의한 선택지 사용
        default='learning',  # 기본값은 '학습중'
        verbose_name="상태"  # 관리자 사이트 등에서 표시될 필드명
    )
    
    # 등록자 필드 - 기술을 등록한 사용자
    author = models.ForeignKey(
        User,  # Django의 내장 User 모델 참조
        on_delete=models.CASCADE,  # 사용자 삭제 시 기술 정보도 함께 삭제
        verbose_name="등록자"  # 관리자 사이트 등에서 표시될 필드명
    )
    
    # 공식 문서 필드 - 기술의 공식 문서나 홈페이지 URL
    official_document = models.URLField(
        blank=True,  # 필수 필드 아님 (비워도 됨)
        verbose_name="공식 문서",  # 관리자 사이트 등에서 표시될 필드명
        help_text="기술의 공식 문서 URL을 입력하세요."  # 입력 도움말
    )
    
    # 학습 자료 필드 - 학습에 도움이 되는 자료나 링크
    learning_resources = models.TextField(
        blank=True,  # 필수 필드 아님 (비워도 됨)
        verbose_name="학습 자료",  # 관리자 사이트 등에서 표시될 필드명
        help_text="학습 자료나 참고 링크를 입력하세요."  # 입력 도움말
    )
    
    # 태그 필드 - 검색 및 분류용 태그
    tags = models.CharField(
        max_length=200,  # 최대 200자까지 허용
        blank=True,  # 필수 필드 아님 (비워도 됨)
        verbose_name="태그",  # 관리자 사이트 등에서 표시될 필드명
        help_text="쉼표로 구분하여 태그를 입력하세요."  # 입력 도움말
    )
    
    # 생성일 필드 - 기술 정보 최초 등록 시간 (자동 설정)
    created_at = models.DateTimeField(
        auto_now_add=True,  # 객체 생성 시 자동으로 현재 시간 저장
        verbose_name="생성일"  # 관리자 사이트 등에서 표시될 필드명
    )
    
    # 수정일 필드 - 기술 정보 수정 시간 (자동 업데이트)
    updated_at = models.DateTimeField(
        auto_now=True,  # 객체 수정 시 자동으로 현재 시간 업데이트
        verbose_name="수정일"  # 관리자 사이트 등에서 표시될 필드명
    )

    class Meta:
        """
        모델 메타데이터 클래스
        
        이 클래스는 모델의 동작과 표현을 제어하는 설정을 포함합니다.
        데이터베이스 테이블 이름, 정렬 순서, 제약 조건 등을 정의합니다.
        """
        verbose_name = '기술'           # 단수 형태의 모델 이름
        verbose_name_plural = '기술들'    # 복수 형태의 모델 이름
        ordering = ['-created_at']      # 기본 정렬 순서 (생성일 최신순)
        
        # 데이터베이스 인덱스 설정 - 검색 성능 향상을 위함
        indexes = [
            models.Index(fields=['category', 'proficiency']),  # 분류와 숙련도 조합 인덱스
            models.Index(fields=['status']),                    # 상태 인덱스
            models.Index(fields=['author']),                    # 등록자 인덱스
        ]
        # 고유 제약 조건 - 동일 사용자가 동일 기술명으로 중복 등록 방지
        unique_together = ['name', 'author']

    def __str__(self):
        """
        모델 인스턴스의 문자열 표현 메서드
        
        관리자 사이트, 디버깅 등에서 객체를 식별할 때 사용됩니다.
        분류와 기술명을 조합하여 반환합니다.
        
        Returns:
            str: "[분류] 기술명" 형식의 문자열
        """
        return f"{self.get_category_display()} - {self.name}"

    def get_absolute_url(self):
        """
        기술 상세 페이지 URL 반환 메서드
        
        템플릿에서 기술 상세 페이지 링크를 생성할 때 사용됩니다.
        
        Returns:
            str: 기술 상세 페이지의 URL
        """
        return reverse('technology_detail', kwargs={'pk': self.pk})

    @property
    def tag_list(self):
        """
        태그를 리스트로 반환하는 프로퍼티
        
        쉼표로 구분된 태그 문자열을 리스트로 변환하여 반환합니다.
        
        Returns:
            list: 태그 문자열 리스트
        """
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()] if self.tags else []

    @property
    def is_completed(self):
        """
        학습 완료 여부 확인 프로퍼티
        
        현재 기술이 학습 완료 상태인지 확인합니다.
        
        Returns:
            bool: 학습 완료 상태이면 True, 아니면 False
        """
        return self.status in ['completed', 'certified']

    @property
    def proficiency_level(self):
        """
        숙련도 레벨을 숫자로 반환하는 프로퍼티
        
        숙련도를 1-4 숫자 레벨로 변환하여 반환합니다.
        
        Returns:
            int: 숙련도 레벨 (1=초급, 2=중급, 3=고급, 4=전문가)
        """
        levels = {'beginner': 1, 'intermediate': 2, 'advanced': 3, 'expert': 4}
        return levels.get(self.proficiency, 1)
