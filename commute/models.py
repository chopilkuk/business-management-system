# =============================================================================
# 비즈니스 관리 시스템 근태 관리 앱 모델
# =============================================================================
# 설명: 근태 관리와 관련된 데이터베이스 모델을 정의
# 작성자: 비즈니스 관리 시스템 개발팀
# 버전: 1.0.0
# =============================================================================

"""
근태 관리 앱의 데이터베이스 모델

이 모듈은 근태 관리와 관련된 데이터베이스 모델을 정의합니다.
직원의 출퇴근 기록, 근무 스케줄 등을 관리합니다.

주요 기능:
- 출퇴근 시간 기록 및 관리
- 근무 시간 자동 계산
- 근태 상태 분류 (정상, 지각, 조퇴, 결근)
- 근무 스케줄 관리
"""

# Django 데이터베이스 모델 임포트
from django.db import models
# Django 기본 사용자 모델 임포트
from django.contrib.auth.models import User
# Django 시간대 관련 유틸리티 임포트
from django.utils import timezone

class CommuteRecord(models.Model):
    """
    근태 기록 모델
    
    이 모델은 직원의 출퇴근 기록을 저장하고 관리합니다.
    출근 시간, 퇴근 시간, 근무 시간, 근태 상태 등을 포함합니다.
    
    Attributes:
        user (ForeignKey): 사용자 (외래키)
        check_in_time (DateTime): 출근 시간
        check_out_time (DateTime): 퇴근 시간
        work_date (Date): 근무일
        total_work_hours (Duration): 총 근무시간
        status (Char): 근태 상태 (normal, late, early_leave, absence)
        notes (TextField): 비고/메모
        created_at (DateTime): 생성일시
        updated_at (DateTime): 수정일시
    """
    
    # =============================================================================
    # 관계 필드
    # =============================================================================
    # 사용자 관계 - 각 근태 기록은 특정 사용자와 연결됨
    # on_delete=models.CASCADE: 사용자가 삭제되면 관련 근태 기록도 함께 삭제
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='사용자')
    
    # =============================================================================
    # 시간 관련 필드들
    # =============================================================================
    # 출근 시간 (선택사항 - 미기록 가능)
    check_in_time = models.DateTimeField(null=True, blank=True, verbose_name='출근 시간')
    
    # 퇴근 시간 (선택사항 - 미기록 가능)
    check_out_time = models.DateTimeField(null=True, blank=True, verbose_name='퇴근 시간')
    
    # 근무일 (필수 - 해당 근태 기록의 날짜)
    work_date = models.DateField(verbose_name='근무일')
    
    # 총 근무시간 (선택사항 - 자동 계산)
    total_work_hours = models.DurationField(null=True, blank=True, verbose_name='총 근무시간')
    
    # =============================================================================
    # 근태 상태 필드
    # =============================================================================
    # 근태 상태 - 선택 가능한 상태들 정의
    status = models.CharField(
        max_length=20,
        choices=[
            ('normal', '정상'),           # 정상 출퇴근
            ('late', '지각'),             # 지각
            ('early_leave', '조퇴'),     # 조퇴
            ('absence', '결근'),         # 결근
        ],
        default='normal',
        verbose_name='근태 상태'
    )
    
    # =============================================================================
    # 추가 정보 필드
    # =============================================================================
    # 비고 또는 메모 (선택사항)
    notes = models.TextField(blank=True, verbose_name='비고')
    
    # =============================================================================
    # 자동 관리 필드들
    # =============================================================================
    # 생성일시 (자동으로 현재 시간 저장)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    
    # 수정일시 (자동으로 현재 시간 저장)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    # =============================================================================
    # 모델 메타데이터 클래스
    # =============================================================================
    class Meta:
        """
        모델 메타데이터 클래스
        
        모델의 동작과 표현을 제어하는 설정을 포함합니다.
        """
        # 단수 형태 모델 이름 (관리자 사이트 등에서 표시)
        verbose_name = '근태 기록'
        
        # 복수 형태 모델 이름
        verbose_name_plural = '근태 기록들'
        
        # 기본 정렬 (최신 근무일, 최신 출근시간 순)
        ordering = ['-work_date', '-check_in_time']
        
        # 복합 유니크 제약조건 - 사용자와 근무일의 조합은 고유해야 함
        unique_together = ['user', 'work_date']

    def __str__(self):
        """
        모델 인스턴스의 문자열 표현
        
        Returns:
            str: 사용자명과 근무일을 조합한 문자열 반환
        """
        return f"{self.user.username} - {self.work_date}"

    def save(self, *args, **kwargs):
        """
        모델 저장 메서드
        
        저장 시 근무 시간과 근태 상태를 자동으로 계산합니다.
        
        Args:
            *args: 위치 인자
            **kwargs: 키워드 인자
        """
        # 출근과 퇴근 시간이 모두 있으면 총 근무시간 계산
        if self.check_in_time and self.check_out_time:
            self.total_work_hours = self.check_out_time - self.check_in_time
            
            # 근태 상태 자동 계산
            # 기준 시간: 9시 출근, 18시 퇴근
            standard_start = timezone.datetime.strptime('09:00', '%H:%M').time()
            standard_end = timezone.datetime.strptime('18:00', '%H:%M').time()
            
            if self.check_in_time.time() > standard_start:
                self.status = 'late'  # 9시 이후 출근은 지각
            elif self.check_out_time.time() < standard_end:
                self.status = 'early_leave'  # 18시 이전 퇴근은 조퇴
            else:
                self.status = 'normal'  # 그 외는 정상
        
        super().save(*args, **kwargs)

    # =============================================================================
    # 프로퍼티 메서드들
    # =============================================================================
    @property
    def is_complete(self):
        """
        완전한 근태 기록 여부 확인
        
        Returns:
            bool: 출근과 퇴근 시간이 모두 기록되었으면 True
        """
        return self.check_in_time is not None and self.check_out_time is not None
    
    @property
    def get_work_hours_display(self):
        """
        근무시간 표시 포맷
        
        Returns:
            str: 근무시간을 시:분 형식으로 반환
        """
        if self.total_work_hours:
            total_seconds = self.total_work_hours.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            return f"{hours}시간 {minutes}분"
        return "미정보"
    
    @property
    def get_status_display_korean(self):
        """
        근태 상태 한국어 표시
        
        Returns:
            str: 근태 상태를 한국어로 반환
        """
        status_dict = {
            'normal': '정상',
            'late': '지각',
            'early_leave': '조퇴',
            'absence': '결근'
        }
        return status_dict.get(self.status, '알 수 없음')

class WorkSchedule(models.Model):
    """
    근무 스케줄 모델
    
    이 모델은 직원의 근무 스케줄을 관리합니다.
    정규근무, 연장근무, 휴일근무, 재택근무 등 다양한 근무 유형을 지원합니다.
    
    Attributes:
        user (ForeignKey): 사용자 (외래키)
        work_date (Date): 근무일
        start_time (Time): 시작 시간
        end_time (Time): 종료 시간
        is_holiday (Boolean): 휴일 여부
        schedule_type (Char): 근무 유형
        notes (TextField): 비고/메모
        created_at (DateTime): 생성일시
        updated_at (DateTime): 수정일시
    """
    
    # =============================================================================
    # 관계 필드
    # =============================================================================
    # 사용자 관계
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='사용자')
    
    # =============================================================================
    # 기본 근무 정보
    # =============================================================================
    # 근무일 (필수)
    work_date = models.DateField(verbose_name='근무일')
    
    # 시작 시간 (필수)
    start_time = models.TimeField(verbose_name='시작 시간')
    
    # 종료 시간 (필수)
    end_time = models.TimeField(verbose_name='종료 시간')
    
    # 휴일 여부 (기본값: False)
    is_holiday = models.BooleanField(default=False, verbose_name='휴일 여부')
    
    # =============================================================================
    # 근무 유형 필드
    # =============================================================================
    # 근무 유형 선택
    schedule_type = models.CharField(
        max_length=20,
        choices=[
            ('regular', '정규근무'),     # 일반적인 정규 근무
            ('overtime', '연장근무'),     # 초과 근무
            ('holiday', '휴일근무'),       # 휴일 근무
            ('remote', '재택근무'),        # 원격 근무
        ],
        default='regular',
        verbose_name='근무 유형'
    )
    
    # =============================================================================
    # 추가 정보 필드
    # =============================================================================
    # 비고 또는 메모 (선택사항)
    notes = models.TextField(blank=True, verbose_name='비고')
    
    # =============================================================================
    # 자동 관리 필드들
    # =============================================================================
    # 생성일시 (자동으로 현재 시간 저장)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    
    # 수정일시 (자동으로 현재 시간 저장)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    # =============================================================================
    # 모델 메타데이터 클래스
    # =============================================================================
    class Meta:
        """
        모델 메타데이터 클래스
        
        모델의 동작과 표현을 제어하는 설정을 포함합니다.
        """
        # 단수 형태 모델 이름
        verbose_name = '근무 스케줄'
        
        # 복수 형태 모델 이름
        verbose_name_plural = '근무 스케줄들'
        
        # 기본 정렬 (근무일, 시작시간 순)
        ordering = ['work_date', 'start_time']
        
        # 복합 유니크 제약조건 - 사용자와 근무일의 조합은 고유해야 함
        unique_together = ['user', 'work_date']

    def __str__(self):
        """
        모델 인스턴스의 문자열 표현
        
        Returns:
            str: 사용자명, 근무일, 근무 유형을 조합한 문자열 반환
        """
        return f"{self.user.username} - {self.work_date} ({self.schedule_type})"

    # =============================================================================
    # 프로퍼티 메서드들
    # =============================================================================
    @property
    def get_work_duration(self):
        """
        근무 시간 계산
        
        Returns:
            datetime.timedelta: 근무 시간을 계산하여 반환
        """
        from datetime import datetime, timedelta
        
        # 시간을 datetime 객체로 변환하여 계산
        start_datetime = datetime.combine(self.work_date, self.start_time)
        end_datetime = datetime.combine(self.work_date, self.end_time)
        
        # 종료 시간이 시작 시간보다 이르면 다음 날로 계산
        if end_datetime < start_datetime:
            end_datetime += timedelta(days=1)
        
        return end_datetime - start_datetime
    
    @property
    def get_work_duration_display(self):
        """
        근무 시간 표시 포맷
        
        Returns:
            str: 근무 시간을 시:분 형식으로 반환
        """
        duration = self.get_work_duration
        hours = int(duration.total_seconds() // 3600)
        minutes = int((duration.total_seconds() % 3600) // 60)
        return f"{hours}시간 {minutes}분"
    
    @property
    def is_weekend(self):
        """
        주말 여부 확인
        
        Returns:
            bool: 근무일이 주말이면 True
        """
        return self.work_date.weekday() >= 5  # 5=토요일, 6=일요일
