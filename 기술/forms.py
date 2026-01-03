from django import forms
from django.core.validators import MinLengthValidator
from .models import Technology


class TechnologyForm(forms.ModelForm):
    """
    기술 관리 폼
    
    기술 정보 등록 및 수정에 사용되는 폼입니다.
    데이터 검증 및 위젯 커스터마이징을 포함합니다.
    """
    
    class Meta:
        model = Technology
        fields = ['name', 'category', 'description', 'proficiency', 'status', 
                 'official_document', 'learning_resources', 'tags']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '기술명을 입력하세요 (예: Python, React, Docker)',
                    'minlength': '2',
                    'required': 'required'
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': '기술에 대한 상세 설명을 입력하세요',
                    'rows': 6
                }
            ),
            'proficiency': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
            'status': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
            'official_document': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '공식 문서 URL을 입력하세요 (선택사항)'
                }
            ),
            'learning_resources': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': '학습 자료나 참고 링크를 입력하세요',
                    'rows': 4
                }
            ),
            'tags': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '태그를 쉼표로 구분하여 입력하세요 (예: 웹, 프레임워크, JavaScript)'
                }
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 필드 레이블 설정
        self.fields['name'].label = '기술명'
        self.fields['category'].label = '분류'
        self.fields['description'].label = '설명'
        self.fields['proficiency'].label = '숙련도'
        self.fields['status'].label = '상태'
        self.fields['official_document'].label = '공식 문서'
        self.fields['learning_resources'].label = '학습 자료'
        self.fields['tags'].label = '태그'
        
        # 필드 헬프 텍스트 설정
        self.fields['name'].help_text = '기술명을 입력하세요. 최소 2자 이상이어야 합니다.'
        self.fields['category'].help_text = '기술의 분류를 선택하세요.'
        self.fields['description'].help_text = '기술에 대한 상세 설명을 입력하세요.'
        self.fields['proficiency'].help_text = '현재 숙련도를 선택하세요.'
        self.fields['status'].help_text = '학습 상태를 선택하세요.'
        self.fields['official_document'].help_text = '기술의 공식 문서나 홈페이지 URL을 입력하세요.'
        self.fields['learning_resources'].help_text = '학습에 도움이 되는 자료나 링크를 입력하세요.'
        self.fields['tags'].help_text = '검색에 도움이 되는 태그를 쉼표로 구분하여 입력하세요.'
    
    def clean_name(self):
        """기술명 검증"""
        name = self.cleaned_data.get('name')
        
        if name:
            # 공백만 있는지 확인
            if name.strip() == '':
                raise forms.ValidationError('기술명에 내용이 포함되어야 합니다.')
            
            # 최소 길이 확인
            if len(name.strip()) < 2:
                raise forms.ValidationError('기술명은 최소 2자 이상이어야 합니다.')
            
            # 최대 길이 확인
            if len(name) > 100:
                raise forms.ValidationError('기술명은 100자 이하이어야 합니다.')
            
            # 특수문자 제한 (알파벳, 숫자, 공백, 하이픈, 언더스크어만 허용)
            import re
            if not re.match(r'^[a-zA-Z0-9\s\-_]+$', name):
                raise forms.ValidationError('기술명은 영문, 숫자, 공백, 하이픈, 언더스코어만 포함할 수 있습니다.')
        
        return name.strip().title()
    
    def clean_description(self):
        """설명 검증"""
        description = self.cleaned_data.get('description')
        
        if description:
            # 공백만 있는지 확인
            if description.strip() == '':
                raise forms.ValidationError('설명에 실제 내용이 포함되어야 합니다.')
            
            # 최소 길이 확인
            if len(description.strip()) < 10:
                raise forms.ValidationError('설명은 최소 10자 이상이어야 합니다.')
        
        return description.strip()
    
    def clean_official_document(self):
        """공식 문서 URL 검증"""
        url = self.cleaned_data.get('official_document')
        
        if url:
            # URL 형식 검증
            if not (url.startswith('http://') or url.startswith('https://')):
                raise forms.ValidationError('URL은 http:// 또는 https://로 시작해야 합니다.')
        
        return url
    
    def clean_tags(self):
        """태그 검증"""
        tags = self.cleaned_data.get('tags')
        
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            
            # 태그 개수 제한
            if len(tag_list) > 10:
                raise forms.ValidationError('태그는 최대 10개까지 입력할 수 있습니다.')
            
            # 태그 길이 제한
            for tag in tag_list:
                if len(tag) > 20:
                    raise forms.ValidationError(f'태그 "{tag}"가 너무 깁니다. 각 태그는 20자 이하이어야 합니다.')
            
            # 중복 태그 제거
            unique_tags = list(dict.fromkeys(tag_list))
            return ', '.join(unique_tags)
        
        return tags
    
    def clean(self):
        """전체 폼 검증"""
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        category = cleaned_data.get('category')
        proficiency = cleaned_data.get('proficiency')
        status = cleaned_data.get('status')
        
        # 자격증 보유 상태는 반드시 고급 이상이어야 함
        if status == 'certified' and proficiency not in ['advanced', 'expert']:
            raise forms.ValidationError('자격증 보유 상태는 고급 또는 전문가 숙련도여야 합니다.')
        
        # 특정 분류의 기술은 해당 숙련도 이상이어야 함
        if category in ['ai', 'devops'] and proficiency in ['beginner']:
            raise forms.ValidationError(f'{self.get_category_display()} 분류의 기술은 초급 숙련도일 수 없습니다.')
        
        return cleaned_data


class TechnologySearchForm(forms.Form):
    """
    기술 검색 폼
    
    기술 검색에 사용되는 폼입니다.
    """
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '기술명이나 태그를 검색하세요',
                'autocomplete': 'off'
            }
        )
    )
    
    category = forms.ChoiceField(
        choices=[('', '전체')] + Technology.CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )
    
    proficiency = forms.ChoiceField(
        choices=[('', '전체')] + Technology.PROFICIENCY_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )
    
    status = forms.ChoiceField(
        choices=[('', '전체')] + Technology.STATUS_CHOICES,
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
        self.fields['category'].label = '분류'
        self.fields['proficiency'].label = '숙련도'
        self.fields['status'].label = '상태'
