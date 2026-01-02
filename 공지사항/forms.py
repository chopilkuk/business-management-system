from django import forms
from django.core.validators import MinLengthValidator
from .models import Notice


class NoticeForm(forms.ModelForm):
    """
    공지사항 폼
    
    공지사항 작성 및 수정에 사용되는 폼입니다.
    데이터 검증 및 위젯 커스터마이징을 포함합니다.
    """
    
    class Meta:
        model = Notice
        fields = ['title', 'content', 'importance', 'status']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '공지사항 제목을 입력하세요 (최소 5자)',
                    'minlength': '5',
                    'required': 'required'
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': '공지사항 내용을 입력하세요',
                    'rows': 10,
                    'required': 'required'
                }
            ),
            'importance': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
            'status': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 필드 레이블 설정
        self.fields['title'].label = '제목'
        self.fields['content'].label = '내용'
        self.fields['importance'].label = '중요도'
        self.fields['status'].label = '상태'
        
        # 필드 헬프 텍스트 설정
        self.fields['title'].help_text = '공지사항 제목을 입력하세요. 최소 5자 이상이어야 합니다.'
        self.fields['content'].help_text = '공지사항 내용을 상세하게 입력하세요.'
        self.fields['importance'].help_text = '공지사항의 중요도를 선택하세요.'
        self.fields['status'].help_text = '공지사항의 상태를 선택하세요.'
    
    def clean_title(self):
        """제목 검증"""
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
        """내용 검증"""
        content = self.cleaned_data.get('content')
        
        if content:
            # 공백만 있는지 확인
            if content.strip() == '':
                raise forms.ValidationError('내용에 실제 내용이 포함되어야 합니다.')
            
            # 최소 길이 확인
            if len(content.strip()) < 10:
                raise forms.ValidationError('내용은 최소 10자 이상이어야 합니다.')
        
        return content.strip()
    
    def clean(self):
        """전체 폼 검증"""
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


class NoticeSearchForm(forms.Form):
    """
    공지사항 검색 폼
    
    공지사항 검색에 사용되는 폼입니다.
    """
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '검색어를 입력하세요',
                'autocomplete': 'off'
            }
        )
    )
    
    importance = forms.ChoiceField(
        choices=[('', '전체')] + Notice.IMPORTANCE_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )
    
    status = forms.ChoiceField(
        choices=[('', '전체')] + Notice.STATUS_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 필드 레이블 설정
        self.fields['search'].label = '검색'
        self.fields['importance'].label = '중요도'
        self.fields['status'].label = '상태'
