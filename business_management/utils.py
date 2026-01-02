"""
일반 유틸리티 함수 모듈

이 모듈은 프로젝트 전체에서 사용되는 일반적인 유틸리티 함수들을 포함합니다.
파일 처리, 날짜 포맷팅, 숫자 포맷팅, 보안 유틸리티 등 다양한 기능을 제공합니다.

주요 기능:
- 파일 업로드 및 검증
- 날짜/시간 포맷팅
- 숫자 및 통화 포맷팅
- 보안 관련 유틸리티
- 이메일 유틸리티
- 페이징 유틸리티

@version 1.0.0
"""

import os
import uuid
from datetime import datetime, date
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from .exceptions import ValidationError, ExternalServiceError
import logging

logger = logging.getLogger(__name__)

class FileHandler:
    """
    파일 처리 유틸리티 클래스
    
    파일 업로드, 검증, 저장 등 파일 관련 작업을 처리합니다.
    보안 검증, 파일 크기 제한, 확장자 검증 등을 포함합니다.
    """
    
    @staticmethod
    def upload_file(file, upload_path='uploads/', allowed_extensions=None, max_size_mb=10):
        """
        파일 업로드 처리
        
        파일을 업로드하고 검증한 후 저장합니다.
        보안 검증, 파일 크기 제한, 확장자 검증을 수행합니다.
        
        Args:
            file: 업로드할 파일 객체
            upload_path: 업로드 경로 (기본값: 'uploads/')
            allowed_extensions: 허용된 파일 확장자 목록 (기본값: None)
            max_size_mb: 최대 파일 크기 (MB) (기본값: 10)
            
        Returns:
            dict: 파일 정보를 포함한 딕셔너리
                - success: 성공 여부
                - file_path: 파일 경로
                - filename: 파일명
                - original_filename: 원본 파일명
                - file_size: 파일 크기
                - file_url: 파일 URL
                
        Raises:
            ValidationError: 파일 검증 실패 시
            ExternalServiceError: 파일 저장 중 오류 발생 시
        """
        try:
            # 파일 검증 수행
            FileHandler._validate_file(file, allowed_extensions, max_size_mb)
            
            # 고유 파일명 생성 (UUID 사용)
            file_extension = os.path.splitext(file.name)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(upload_path, unique_filename)
            
            # 파일 저장
            path = default_storage.save(file_path, ContentFile(file.read()))
            
            return {
                'success': True,
                'file_path': path,
                'filename': unique_filename,
                'original_filename': file.name,
                'file_size': file.size,
                'file_url': default_storage.url(path)
            }
            
        except Exception as e:
            logger.error(f"File upload error: {str(e)}")
            if isinstance(e, ValidationError):
                raise e
            raise ExternalServiceError("파일 업로드 중 오류가 발생했습니다.")
    
    @staticmethod
    def _validate_file(file, allowed_extensions, max_size_mb):
        """
        파일 검증 수행
        
        파일의 크기, 확장자, MIME 타입 등을 검증합니다.
        
        Args:
            file: 검증할 파일 객체
            allowed_extensions: 허용된 확장자 목록
            max_size_mb: 최대 파일 크기 (MB)
            
        Raises:
            ValidationError: 검증 실패 시
        """
        # 파일 존재 여부 검증
        if not file:
            raise ValidationError("파일이 선택되지 않았습니다.")
        
        # 파일 크기 검증
        max_size_bytes = max_size_mb * 1024 * 1024  # MB를 바이트로 변환
        if file.size > max_size_bytes:
            raise ValidationError(f"파일 크기는 {max_size_mb}MB를 초과할 수 없습니다.")
        
        # 파일 확장자 검증
        if allowed_extensions:
            file_extension = os.path.splitext(file.name)[1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError(f"허용되지 않는 파일 형식입니다: {file_extension}")
        
        # 파일 내용 검증 (기본적인 MIME 타입 검증)
        if hasattr(file, 'content_type'):
            # 허용된 MIME 타입 목록
            allowed_mime_types = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.pdf': 'application/pdf',
                '.doc': 'application/msword',
                '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                '.xls': 'application/vnd.ms-excel',
                '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                '.txt': 'text/plain',
                '.csv': 'text/csv'
            }
            
            file_extension = os.path.splitext(file.name)[1].lower()
            expected_mime = allowed_mime_types.get(file_extension)
            
            if expected_mime and file.content_type != expected_mime:
                logger.warning(f"MIME type mismatch: {file.name} - Expected: {expected_mime}, Got: {file.content_type}")

class DateFormatter:
    """
    날짜 포맷 유틸리티 클래스
    
    날짜와 시간을 다양한 형식으로 포맷팅합니다.
    한국어 날짜 표시, 평일 계산 등을 지원합니다.
    """
    
    @staticmethod
    def format_korean_date(date_obj, format_type='full'):
        """
        한국 날짜 포맷
        
        날짜 객체를 한국어 형식으로 포맷팅합니다.
        
        Args:
            date_obj: 날짜 객체 (datetime, date, string)
            format_type: 포맷 타입 ('full', 'short', 'time', 'datetime')
                - full: 'YYYY년 MM월 DD일'
                - short: 'YY.MM.DD'
                - time: 'HH:mm'
                - datetime: 'YYYY년 MM월 DD일 HH:mm'
                
        Returns:
            str: 포맷된 날짜 문자열
        """
        # 문자열 날짜를 datetime 객체로 변환
        if isinstance(date_obj, str):
            try:
                date_obj = datetime.strptime(date_obj, '%Y-%m-%d').date()
            except ValueError:
                try:
                    date_obj = datetime.strptime(date_obj, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    return date_obj  # 변환 실패 시 원본 반환
        
        # 포맷 타입에 따른 포맷팅
        if format_type == 'full':
            return date_obj.strftime('%Y년 %m월 %d일')
        elif format_type == 'short':
            return date_obj.strftime('%y.%m.%d')
        elif format_type == 'time':
            return date_obj.strftime('%H:%M')
        elif format_type == 'datetime':
            return date_obj.strftime('%Y년 %m월 %d일 %H:%M')
        else:
            return date_obj.strftime('%Y-%m-%d')
    
    @staticmethod
    def get_business_days(start_date, end_date):
        """
        평일 계산 (주말 제외)
        
        두 날짜 사이의 평일 수를 계산합니다.
        주말(토요일, 일요일)은 제외합니다.
        
        Args:
            start_date: 시작일 (datetime, date, string)
            end_date: 종료일 (datetime, date, string)
            
        Returns:
            int: 평일 수
        """
        from datetime import timedelta
        
        # 문자열 날짜를 date 객체로 변환
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        business_days = 0
        current_date = start_date
        
        # 시작일부터 종료일까지 순회하며 평일 계산
        while current_date <= end_date:
            if current_date.weekday() < 5:  # 월요일(0) ~ 금요일(4)
                business_days += 1
            current_date += timedelta(days=1)
        
        return business_days

class NumberFormatter:
    """
    숫자 포맷 유틸리티 클래스
    
    숫자를 다양한 형식으로 포맷팅합니다.
    통화, 전화번호 등을 포맷팅합니다.
    """
    
    @staticmethod
    def format_korean_currency(amount):
        """
        한국 통화 포맷
        
        숫자를 한국 통화 형식으로 포맷팅합니다.
        
        Args:
            amount: 금액 (int, float, string)
            
        Returns:
            str: 포맷된 금액 문자열 (예: '1,000,000원')
            
        Raises:
            ValueError: 숫자 변환 실패 시
        """
        try:
            # 문자열을 정수로 변환
            if isinstance(amount, str):
                amount = int(amount.replace(',', ''))
            
            # 천 단위 구분자 추가
            return f"{amount:,}원"
        except (ValueError, TypeError):
            return "0원"
    
    @staticmethod
    def format_phone_number(phone_number):
        """
        전화번호 포맷
        
        전화번호를 한국 표준 형식으로 포맷팅합니다.
        
        Args:
            phone_number: 전화번호 문자열
            
        Returns:
            str: 포맷된 전화번호
                - 10자리: '02-XXXX-XXXX' (서울 지역번호)
                - 11자리: '010-XXXX-XXXX' (휴대폰)
                - 기타: 원본 반환
        """
        # 숫자만 추출
        numbers = ''.join(filter(str.isdigit, phone_number))
        
        # 길이에 따른 포맷팅
        if len(numbers) == 10:
            # 02-XXXX-XXXX 형식 (서울 지역번호)
            return f"{numbers[:2]}-{numbers[2:6]}-{numbers[6:]}"
        elif len(numbers) == 11:
            # 010-XXXX-XXXX 형식 (휴대폰)
            return f"{numbers[:3]}-{numbers[3:7]}-{numbers[7:]}"
        else:
            return phone_number  # 기타 경우 원본 반환

class BusinessNumberFormatter:
    """
    사업자등록번호 포맷 유틸리티 클래스
    
    사업자등록번호를 표준 형식으로 포맷팅합니다.
    """
    
    @staticmethod
    def format_business_number(number):
        """
        사업자등록번호 포맷
        
        사업자등록번호를 표준 형식으로 포맷팅합니다.
        
        Args:
            number: 사업자등록번호 문자열
            
        Returns:
            str: 포맷된 사업자등록번호 (예: '123-45-67890')
        """
        # 숫자만 추출
        numbers = ''.join(filter(str.isdigit, number))
        
        # 10자리인 경우에만 포맷팅
        if len(numbers) == 10:
            return f"{numbers[:3]}-{numbers[3:5]}-{numbers[5:]}"
        else:
            return number  # 기타 경우 원본 반환

class SecurityUtils:
    """
    보안 유틸리티 클래스
    
    보안 관련 유틸리티 함수들을 제공합니다.
    데이터 마스킹, 토큰 생성 등을 지원합니다.
    """
    
    @staticmethod
    def mask_sensitive_data(data, mask_char='*', visible_chars=4):
        """
        민감한 데이터 마스킹
        
        민감한 데이터의 일부를 마스킹 처리합니다.
        주로 로그 출력 시 사용됩니다.
        
        Args:
            data: 마스킹할 데이터
            mask_char: 마스킹 문자 (기본값: '*')
            visible_chars: 보여줄 문자 수 (기본값: 4)
            
        Returns:
            str: 마스킹된 데이터
        """
        if not data or len(data) <= visible_chars:
            return mask_char * len(data) if data else data
        
        # 마지막 visible_chars개만 보여주고 나머지는 마스킹
        visible_part = data[-visible_chars:]
        masked_part = mask_char * (len(data) - visible_chars)
        
        return masked_part + visible_part
    
    @staticmethod
    def generate_secure_token(length=32):
        """
        보안 토큰 생성
        
        안전한 무작위 토큰을 생성합니다.
        세션 키, API 키 등에 사용됩니다.
        
        Args:
            length: 토큰 길이 (기본값: 32)
            
        Returns:
            str: 보안 토큰
        """
        import secrets
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        return ''.join(secrets.choice(alphabet) for _ in range(length))

class EmailUtils:
    """
    이메일 유틸리티 클래스
    
    이메일 관련 유틸리티 함수들을 제공합니다.
    """
    
    @staticmethod
    def validate_email_format(email):
        """
        이메일 형식 검증
        
        이메일 주소의 형식이 올바른지 검증합니다.
        
        Args:
            email: 검증할 이메일 주소
            
        Returns:
            bool: 유효성 여부
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def extract_domain(email):
        """
        이메일에서 도메인 추출
        
        이메일 주소에서 도메인 부분만 추출합니다.
        
        Args:
            email: 이메일 주소
            
        Returns:
            str: 도메인
        """
        try:
            return email.split('@')[1].lower()
        except (IndexError, AttributeError):
            return ''

class PaginationUtils:
    """
    페이징 유틸리티 클래스
    
    페이징 관련 유틸리티 함수들을 제공합니다.
    """
    
    @staticmethod
    def get_pagination_info(page_obj, request_path=''):
        """
        페이징 정보 생성
        
        Django 페이지 객체에서 페이징 정보를 추출합니다.
        
        Args:
            page_obj: Django 페이지 객체
            request_path: 요청 경로 (기본값: '')
            
        Returns:
            dict: 페이징 정보를 포함한 딕셔너리
                - current_page: 현재 페이지 번호
                - total_pages: 전체 페이지 수
                - total_items: 전체 아이템 수
                - items_per_page: 페이지당 아이템 수
                - has_previous: 이전 페이지 존재 여부
                - has_next: 다음 페이지 존재 여부
                - previous_page: 이전 페이지 번호
                - next_page: 다음 페이지 번호
                - start_index: 시작 인덱스
                - end_index: 종료 인덱스
        """
        return {
            'current_page': page_obj.number,
            'total_pages': page_obj.paginator.num_pages,
            'total_items': page_obj.paginator.count,
            'items_per_page': page_obj.paginator.per_page,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
            'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
            'start_index': page_obj.start_index(),
            'end_index': page_obj.end_index()
        }
