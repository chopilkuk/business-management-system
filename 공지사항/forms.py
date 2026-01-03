# =============================================================================
# 비즈니스 관리 시스템 공지사항 앱 폼
# =============================================================================
# 설명: 공지사항 관리와 관련된 폼 클래스를 정의
# 작성자: 비즈니스 관리 시스템 개발팀
# 버전: 1.0.0
# =============================================================================

# =============================================================================
# 임포트 구역
# =============================================================================
# Django 폼 모듈 임포트
from django import forms
# Django 최소 길이 검증기 임포트
from django.core.validators import MinLengthValidator
# 현재 앱의 모델 임포트
from .models import Notice

# =============================================================================
# 공지사항 작성/수정 폼 클래스
# =============================================================================
class NoticeForm(forms.ModelForm):
    """
    공지사항 폼 클래스
    
    공지사항 작성 및 수정에 사용되는 폼입니다.
    데이터 검증 및 위젯 커스터마이징을 포함합니다.
    
    Features:
        - 제목, 내용, 중요도, 상태 필드 포함
        - Bootstrap CSS 클래스 적용
        - 커스텀 데이터 검증 로직
        - 필드별 유효성 검증
        - 사용자 친화적인 에러 메시지
        
    Validation Rules:
        - 제목: 최소 5자, 최대 200자
        - 내용: 최소 10자
        - 긴급 공지사항은 반드시 게시 상태
        - 제목과 내용의 중복 방지
        
    Attributes:
        title: 공지사항 제목 필드
        content: 공지사항 내용 필드
        importance: 중요도 선택 필드
        status: 상태 선택 필드
    """
    
    # =============================================================================
    # 메타 클래스 설정
    # =============================================================================
    class Meta:
        """
        폼 메타데이터 클래스
        
        폼의 기본 설정과 위젯 커스터마이징을 정의합니다.
        """
        model = Notice  # 연결할 모델
        fields = ['title', 'content', 'importance', 'status']  # 포함할 필드 목록
        
        # 필드별 위젯 커스터마이징
        widgets = {
            # 제목 필드: 텍스트 입력 위젯
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',  # Bootstrap CSS 클래스
                    'placeholder': '공지사항 제목을 입력하세요 (최소 5자)',  # 플레이스홀더
                    'minlength': '5',  # HTML5 최소 길이 제한
                    'required': 'required'  # 필수 필드 표시
                }
            ),
            
            # 내용 필드: 텍스트 영역 위젯
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',  # Bootstrap CSS 클래스
                    'placeholder': '공지사항 내용을 입력하세요',  # 플레이스홀더
                    'rows': 10,  # 텍스트 영역 높이
                    'required': 'required'  # 필수 필드 표시
                }
            ),
            
            # 중요도 필드: 선택 위젯
            'importance': forms.Select(
                attrs={
                    'class': 'form-select'  # Bootstrap CSS 클래스
                }
            ),
            
            # 상태 필드: 선택 위젯
            'status': forms.Select(
                attrs={
                    'class': 'form-select'  # Bootstrap CSS 클래스
                }
            ),
        }
    
    # =============================================================================
    # 폼 초기화 메서드
    # =============================================================================
    def __init__(self, *args, **kwargs):
        """
        폼 초기화 메서드
        
        폼 필드의 레이블과 헬프 텍스트를 설정합니다.
        
        Args:
            *args: 위치 인자
            **kwargs: 키워드 인자
        """
        super().__init__(*args, **kwargs)
        
        # 필드 레이블 설정 (한국어)
        self.fields['title'].label = '제목'
        self.fields['content'].label = '내용'
        self.fields['importance'].label = '중요도'
        self.fields['status'].label = '상태'
        
        # 필드 헬프 텍스트 설정 (사용자 안내)
        self.fields['title'].help_text = '공지사항 제목을 입력하세요. 최소 5자 이상이어야 합니다.'
        self.fields['content'].help_text = '공지사항 내용을 상세하게 입력하세요.'
        self.fields['importance'].help_text = '공지사항의 중요도를 선택하세요.'
        self.fields['status'].help_text = '공지사항의 상태를 선택하세요.'
    
    # =============================================================================
    # 개별 필드 검증 메서드들
    # =============================================================================
    def clean_title(self):
        """
        제목 필드 검증 메서드
        
        제목의 유효성을 검증합니다.
        
        Returns:
            str: 검증된 제목 문자열
            
        Raises:
            ValidationError: 제목이 유효하지 않을 경우
            
        Validation Rules:
            - 공백만 있는지 확인
            - 최소 길이 확인 (5자)
            - 최대 길이 확인 (200자)
        """
        title = self.cleaned_data.get('title')
        
        if title:
            # 공백만 있는지 확인
            if title.strip() == '':
                raise forms.ValidationError('제목에 내용이 포함되어야 합니다.')
            
            # 최소 길이 확인
            if len(title.strip()) < 5:
                raise forms.ValidationError('제목은 최소 5자 이상이어야 합니다.')
            
            # 최대 길이 확인
            if len(title) > 200:
                raise forms.ValidationError('제목은 200자 이하이어야 합니다.')
        
        return title.strip()
    
    def clean_content(self):
        """
        내용 필드 검증 메서드
        
        내용의 유효성을 검증합니다.
        
        Returns:
            str: 검증된 내용 문자열
            
        Raises:
            ValidationError: 내용이 유효하지 않을 경우
            
        Validation Rules:
            - 공백만 있는지 확인
            - 최소 길이 확인 (10자)
        """
        content = self.cleaned_data.get('content')
        
        if content:
            # 공백만 있는지 확인
            if content.strip() == '':
                raise forms.ValidationError('내용에 실제 내용이 포함되어야 합니다.')
            
            # 최소 길이 확인
            if len(content.strip()) < 10:
                raise forms.ValidationError('내용은 최소 10자 이상이어야 합니다.')
        
        return content.strip()
    
    # =============================================================================
    # 전체 폼 검증 메서드
    # =============================================================================
    def clean(self):
        """
        전체 폼 검증 메서드
        
        여러 필드 간의 관계를 검증합니다.
        
        Returns:
            dict: 검증된 cleaned_data
            
        Raises:
            ValidationError: 필드 간의 관계가 유효하지 않을 경우
            
        Validation Rules:
            - 긴급 공지사항은 반드시 게시 상태여야 함
            - 제목과 내용의 중복 방지
        """
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        importance = cleaned_data.get('importance')
        status = cleaned_data.get('status')
        
        # 긴급 공지사항은 반드시 게시 상태여야 함
        if importance == 'urgent' and status != 'published':
            raise forms.ValidationError('긴급 공지사항은 반드시 게시 상태여야 합니다.')
        
        # 제목과 내용의 중복 확인
        if title and content:
            if title.lower() == content.lower()[:len(title)]:
                raise forms.ValidationError('제목과 내용이 너무 유사합니다. 내용을 더 구체적으로 작성해주세요.')
        
        return cleaned_data

# =============================================================================
# 공지사항 검색 폼 클래스
# =============================================================================
class NoticeSearchForm(forms.Form):
    """
    공지사항 검색 폼 클래스
    
    공지사항 검색에 사용되는 폼입니다.
    검색어, 중요도, 상태 필터링 기능을 제공합니다.
    
    Features:
        - 검색어 입력 필드
        - 중요도 필터링
        - 상태 필터링
        - Bootstrap CSS 클래스 적용
        - 필수가 아닌 선택적 필드
        
    Fields:
        search: 검색어 필드
        importance: 중요도 필터 필드
        status: 상태 필터 필드
    """
    
    # =============================================================================
    # 검색 필드 정의
    # =============================================================================
    # 검색어 필드
    search = forms.CharField(
        max_length=100,  # 최대 길이 100자
        required=False,  # 필수가 아님
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',  # Bootstrap CSS 클래스
                'placeholder': '검색어를 입력하세요',  # 플레이스홀더
                'autocomplete': 'off'  # 자동완성 비활성화
            }
        )
    )
    
    # 중요도 필터 필드
    importance = forms.ChoiceField(
        choices=[('', '전체')] + Notice.IMPORTANCE_CHOICES,  # 전체 옵션 추가
        required=False,  # 필수가 아님
        widget=forms.Select(
            attrs={
                'class': 'form-select'  # Bootstrap CSS 클래스
            }
        )
    )
    
    # 상태 필터 필드
    status = forms.ChoiceField(
        choices=[('', '전체')] + Notice.STATUS_CHOICES,  # 전체 옵션 추가
        required=False,  # 필수가 아님
        widget=forms.Select(
            attrs={
                'class': 'form-select'  # Bootstrap CSS 클래스
            }
        )
    )
    
    # =============================================================================
    # 폼 초기화 메서드
    # =============================================================================
    def __init__(self, *args, **kwargs):
        """
        검색 폼 초기화 메서드
        
        필드의 레이블을 설정합니다.
        
        Args:
            *args: 위치 인자
            **kwargs: 키워드 인자
        """
        super().__init__(*args, **kwargs)
        
        # 필드 레이블 설정 (한국어)
        self.fields['search'].label = '검색'
        self.fields['importance'].label = '중요도'
        self.fields['status'].label = '상태'
