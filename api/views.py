# =============================================================================
# 비즈니스 관리 시스템 RESTful API 뷰
# =============================================================================
# 설명: 시스템의 모든 데이터에 대한 RESTful API 엔드포인트를 제공
# 작성자: 비즈니스 관리 시스템 개발팀
# 버전: 1.0.0
# =============================================================================

"""
RESTful API 뷰 모듈

이 모듈은 시스템의 모든 데이터에 대한 RESTful API 엔드포인트를 제공합니다.
JSON 응답, 에러 처리, 인증, 권한 관리 등을 포함합니다.

주요 기능:
- 공지사항 API
- 기술 관리 API
- 거래처 정보 API
- 사용자 관리 API
- 검색 및 필터링 API
"""

# =============================================================================
# 임포트 구역
# =============================================================================
# Django HTTP 응답 클래스 임포트
from django.http import JsonResponse, HttpResponse
# CSRF 보호 데코레이터 임포트
from django.views.decorators.csrf import csrf_exempt
# HTTP 메서드 제한 데코레이터 임포트
from django.views.decorators.http import require_http_methods
# 로그인 요구 데코레이터 임포트
from django.contrib.auth.decorators import login_required
# 페이지네이터 임포트
from django.core.paginator import Paginator
# 복잡한 데이터베이스 쿼리를 위한 Q 객체 임포트
from django.db.models import Q
# 메서드 데코레이터 임포트
from django.utils.decorators import method_decorator
# Django 뷰 클래스 임포트
from django.views import View
# Django 직렬화 임포트
from django.core import serializers
# 표준 라이브러리 임포트
import json
import logging
from datetime import datetime

# =============================================================================
# 모델 임포트 (동적 임포트)
# =============================================================================
# Django 설정이 로드된 후에만 모델을 임포트하여 순환 참조 방지
try:
    from 공지사항.models import Notice
    from 기술.models import Technology
    from client_inform.models import customer_information
    from django.contrib.auth import get_user_model
    User = get_user_model()
    MODELS_AVAILABLE = True
except ImportError:
    # 모델을 사용할 수 없는 경우 (예: 마이그레이션 전)
    MODELS_AVAILABLE = False
    User = None

# =============================================================================
# 로거 설정
# =============================================================================
# API 전용 로거 설정 - 디버깅 및 모니터링용
api_logger = logging.getLogger('api')

# =============================================================================
# API 응답 표준 클래스
# =============================================================================
class APIResponse:
    """
    API 응답 표준 클래스
    
    모든 API 엔드포인트에서 일관된 응답 형식을 제공합니다.
    성공, 오류, 페이지네이션 등 다양한 응답 타입을 지원합니다.
    
    Methods:
        success: 성공 응답 생성
        error: 오류 응답 생성
        paginated: 페이지네이션 응답 생성
        
    Response Format:
        - success: 성공 여부 (boolean)
        - message: 응답 메시지 (string)
        - data: 응답 데이터 (object/array)
        - error_code: 오류 코드 (string, optional)
        - details: 상세 오류 정보 (object, optional)
        - timestamp: 응답 시간 (ISO 8601 format)
    """
    
    @staticmethod
    def success(data=None, message="성공", status=200):
        """
        성공 응답 생성 메서드
        
        Args:
            data (object/array): 응답 데이터
            message (str): 성공 메시지
            status (int): HTTP 상태 코드
            
        Returns:
            JsonResponse: 표준화된 성공 응답
            
        Description:
            - API 호출 성공 시 표준 응답 생성
            - 일관된 성공 응답 형식 제공
            - 타임스탬프 자동 추가
            - 데이터 포맷 자동 직렬화
        """
        response_data = {
            'success': True,
            'message': message,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        return JsonResponse(response_data, status=status)
    
    @staticmethod
    def error(message="오류 발생", status=400, error_code=None, details=None):
        """
        오류 응답 생성 메서드
        
        Args:
            message (str): 오류 메시지
            status (int): HTTP 상태 코드
            error_code (str): 오류 코드
            details (object): 상세 오류 정보
            
        Returns:
            JsonResponse: 표준화된 오류 응답
            
        Description:
            - API 호출 실패 시 표준 오류 응답 생성
            - 일관된 오류 응답 형식 제공
            - 오류 코드 및 상세 정보 포함
            - 타임스탬프 자동 추가
        """
        response_data = {
            'success': False,
            'message': message,
            'error_code': error_code,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        return JsonResponse(response_data, status=status)
    
    @staticmethod
    def paginated(queryset, page=1, per_page=10):
        """
        페이지네이션 응답 생성 메서드
        
        Args:
            queryset: 데이터베이스 쿼리셋
            page (int): 현재 페이지 번호
            per_page (int): 페이지당 항목 수
            
        Returns:
            JsonResponse: 페이지네이션된 응답
            
        Description:
            - 대용량 데이터를 페이지별로 제공
            - 페이지네이션 정보 포함
            - 이전/다음 페이지 링크 제공
            - 총 항목 수 및 페이지 수 정보
        """
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        data = {
            'items': list(page_obj.object_list.values()),
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
                'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
                'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
                'per_page': per_page
            }
        }
        
        return APIResponse.success(data)


class NoticeAPIView(View):
    """공지사항 API 뷰"""
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, pk=None):
        """공지사항 목록 또는 상세 조회"""
        try:
            if not MODELS_AVAILABLE:
                return APIResponse.error("모델을 사용할 수 없습니다.", status=500)
            
            if pk:
                # 상세 조회
                notice = Notice.objects.get(pk=pk)
                data = {
                    'id': notice.id,
                    'title': notice.title,
                    'content': notice.content,
                    'author': notice.author.username,
                    'importance': notice.importance,
                    'importance_display': notice.get_importance_display(),
                    'status': notice.status,
                    'status_display': notice.get_status_display(),
                    'view_count': notice.view_count,
                    'created_at': notice.created_at.isoformat(),
                    'updated_at': notice.updated_at.isoformat(),
                    'published_at': notice.published_at.isoformat() if notice.published_at else None,
                    'is_published': notice.is_published,
                    'is_urgent': notice.is_urgent,
                    'can_edit': notice.author == request.user or request.user.is_staff,
                    'can_delete': notice.author == request.user or request.user.is_staff,
                    'can_publish': notice.author == request.user or request.user.is_staff,
                    'can_archive': notice.author == request.user or request.user.is_staff,
                }
                return APIResponse.success(data)
            else:
                # 목록 조회
                queryset = Notice.objects.all()
                
                # 검색
                search = request.GET.get('search', '')
                if search:
                    queryset = queryset.filter(
                        Q(title__icontains=search) | Q(content__icontains=search)
                    )
                
                # 필터링
                importance = request.GET.get('importance', '')
                if importance:
                    queryset = queryset.filter(importance=importance)
                
                status = request.GET.get('status', '')
                if status:
                    queryset = queryset.filter(status=status)
                
                # 일반 사용자는 게시된 공지만 볼 수 있음
                if not request.user.is_staff:
                    queryset = queryset.filter(status='published')
                
                # 정렬
                queryset = queryset.order_by('-created_at')
                
                # 페이지네이션
                page = int(request.GET.get('page', 1))
                per_page = int(request.GET.get('per_page', 10))
                
                return APIResponse.paginated(queryset, page, per_page)
                
        except Notice.DoesNotExist:
            return APIResponse.error("공지사항을 찾을 수 없습니다.", 404, "NOTICE_NOT_FOUND")
        except Exception as e:
            api_logger.error(f"공지사항 조회 오류: {str(e)}")
            return APIResponse.error("서버 오류가 발생했습니다.", 500, "SERVER_ERROR")
    
    def post(self, request):
        """공지사항 생성"""
        try:
            data = json.loads(request.body)
            
            # 필수 필드 검증
            if not data.get('title') or not data.get('content'):
                return APIResponse.error("제목과 내용은 필수입니다.", 400, "MISSING_REQUIRED_FIELDS")
            
            # 공지사항 생성
            notice = Notice.objects.create(
                title=data['title'],
                content=data['content'],
                author=request.user,
                importance=data.get('importance', 'medium'),
                status=data.get('status', 'draft')
            )
            
            # 자동 게시 옵션
            if data.get('auto_publish'):
                notice.status = 'published'
                notice.save()
            
            return APIResponse.success(
                {'id': notice.id, 'message': '공지사항이 성공적으로 생성되었습니다.'},
                status=201
            )
            
        except json.JSONDecodeError:
            return APIResponse.error("잘못된 JSON 형식입니다.", 400, "INVALID_JSON")
        except Exception as e:
            api_logger.error(f"공지사항 생성 오류: {str(e)}")
            return APIResponse.error("서버 오류가 발생했습니다.", 500, "SERVER_ERROR")
    
    def put(self, request, pk):
        """공지사항 수정"""
        try:
            notice = Notice.objects.get(pk=pk)
            
            # 권한 확인
            if notice.author != request.user and not request.user.is_staff:
                return APIResponse.error("수정 권한이 없습니다.", 403, "PERMISSION_DENIED")
            
            data = json.loads(request.body)
            
            # 필드 업데이트
            if 'title' in data:
                notice.title = data['title']
            if 'content' in data:
                notice.content = data['content']
            if 'importance' in data:
                notice.importance = data['importance']
            if 'status' in data:
                notice.status = data['status']
            
            notice.save()
            
            return APIResponse.success(
                {'id': notice.id, 'message': '공지사항이 성공적으로 수정되었습니다.'}
            )
            
        except Notice.DoesNotExist:
            return APIResponse.error("공지사항을 찾을 수 없습니다.", 404, "NOTICE_NOT_FOUND")
        except json.JSONDecodeError:
            return APIResponse.error("잘못된 JSON 형식입니다.", 400, "INVALID_JSON")
        except Exception as e:
            api_logger.error(f"공지사항 수정 오류: {str(e)}")
            return APIResponse.error("서버 오류가 발생했습니다.", 500, "SERVER_ERROR")
    
    def delete(self, request, pk):
        """공지사항 삭제"""
        try:
            notice = Notice.objects.get(pk=pk)
            
            # 권한 확인
            if notice.author != request.user and not request.user.is_staff:
                return APIResponse.error("삭제 권한이 없습니다.", 403, "PERMISSION_DENIED")
            
            notice.delete()
            
            return APIResponse.success(
                {'message': '공지사항이 성공적으로 삭제되었습니다.'}
            )
            
        except Notice.DoesNotExist:
            return APIResponse.error("공지사항을 찾을 수 없습니다.", 404, "NOTICE_NOT_FOUND")
        except Exception as e:
            api_logger.error(f"공지사항 삭제 오류: {str(e)}")
            return APIResponse.error("서버 오류가 발생했습니다.", 500, "SERVER_ERROR")


class TechnologyAPIView(View):
    """기술 관리 API 뷰"""
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, pk=None):
        """기술 목록 또는 상세 조회"""
        try:
            if pk:
                # 상세 조회
                tech = Technology.objects.get(pk=pk)
                data = {
                    'id': tech.id,
                    'name': tech.name,
                    'category': tech.category,
                    'category_display': tech.get_category_display(),
                    'description': tech.description,
                    'proficiency': tech.proficiency,
                    'proficiency_display': tech.get_proficiency_display(),
                    'status': tech.status,
                    'status_display': tech.get_status_display(),
                    'author': tech.author.username,
                    'official_document': tech.official_document,
                    'learning_resources': tech.learning_resources,
                    'tags': tech.tags,
                    'tag_list': tech.tag_list,
                    'is_completed': tech.is_completed,
                    'proficiency_level': tech.proficiency_level,
                    'created_at': tech.created_at.isoformat(),
                    'updated_at': tech.updated_at.isoformat(),
                    'can_edit': tech.author == request.user or request.user.is_staff,
                    'can_delete': tech.author == request.user or request.user.is_staff,
                }
                return APIResponse.success(data)
            else:
                # 목록 조회
                queryset = Technology.objects.all()
                
                # 검색
                search = request.GET.get('search', '')
                if search:
                    queryset = queryset.filter(
                        Q(name__icontains=search) | 
                        Q(description__icontains=search) |
                        Q(tags__icontains=search)
                    )
                
                # 필터링
                category = request.GET.get('category', '')
                if category:
                    queryset = queryset.filter(category=category)
                
                proficiency = request.GET.get('proficiency', '')
                if proficiency:
                    queryset = queryset.filter(proficiency=proficiency)
                
                status = request.GET.get('status', '')
                if status:
                    queryset = queryset.filter(status=status)
                
                # 정렬
                queryset = queryset.order_by('-created_at')
                
                # 페이지네이션
                page = int(request.GET.get('page', 1))
                per_page = int(request.GET.get('per_page', 10))
                
                return APIResponse.paginated(queryset, page, per_page)
                
        except Technology.DoesNotExist:
            return APIResponse.error("기술 정보를 찾을 수 없습니다.", 404, "TECHNOLOGY_NOT_FOUND")
        except Exception as e:
            api_logger.error(f"기술 조회 오류: {str(e)}")
            return APIResponse.error("서버 오류가 발생했습니다.", 500, "SERVER_ERROR")
    
    def post(self, request):
        """기술 생성"""
        try:
            data = json.loads(request.body)
            
            # 필수 필드 검증
            if not data.get('name'):
                return APIResponse.error("기술명은 필수입니다.", 400, "MISSING_REQUIRED_FIELDS")
            
            # 기술 생성
            tech = Technology.objects.create(
                name=data['name'],
                category=data.get('category', 'etc'),
                description=data.get('description', ''),
                proficiency=data.get('proficiency', 'beginner'),
                status=data.get('status', 'learning'),
                author=request.user,
                official_document=data.get('official_document', ''),
                learning_resources=data.get('learning_resources', ''),
                tags=data.get('tags', '')
            )
            
            return APIResponse.success(
                {'id': tech.id, 'message': '기술 정보가 성공적으로 생성되었습니다.'},
                status=201
            )
            
        except json.JSONDecodeError:
            return APIResponse.error("잘못된 JSON 형식입니다.", 400, "INVALID_JSON")
        except Exception as e:
            api_logger.error(f"기술 생성 오류: {str(e)}")
            return APIResponse.error("서버 오류가 발생했습니다.", 500, "SERVER_ERROR")
    
    def put(self, request, pk):
        """기술 수정"""
        try:
            tech = Technology.objects.get(pk=pk)
            
            # 권한 확인
            if tech.author != request.user and not request.user.is_staff:
                return APIResponse.error("수정 권한이 없습니다.", 403, "PERMISSION_DENIED")
            
            data = json.loads(request.body)
            
            # 필드 업데이트
            if 'name' in data:
                tech.name = data['name']
            if 'category' in data:
                tech.category = data['category']
            if 'description' in data:
                tech.description = data['description']
            if 'proficiency' in data:
                tech.proficiency = data['proficiency']
            if 'status' in data:
                tech.status = data['status']
            if 'official_document' in data:
                tech.official_document = data['official_document']
            if 'learning_resources' in data:
                tech.learning_resources = data['learning_resources']
            if 'tags' in data:
                tech.tags = data['tags']
            
            tech.save()
            
            return APIResponse.success(
                {'id': tech.id, 'message': '기술 정보가 성공적으로 수정되었습니다.'}
            )
            
        except Technology.DoesNotExist:
            return APIResponse.error("기술 정보를 찾을 수 없습니다.", 404, "TECHNOLOGY_NOT_FOUND")
        except json.JSONDecodeError:
            return APIResponse.error("잘못된 JSON 형식입니다.", 400, "INVALID_JSON")
        except Exception as e:
            api_logger.error(f"기술 수정 오류: {str(e)}")
            return APIResponse.error("서버 오류가 발생했습니다.", 500, "SERVER_ERROR")
    
    def delete(self, request, pk):
        """기술 삭제"""
        try:
            tech = Technology.objects.get(pk=pk)
            
            # 권한 확인
            if tech.author != request.user and not request.user.is_staff:
                return APIResponse.error("삭제 권한이 없습니다.", 403, "PERMISSION_DENIED")
            
            tech.delete()
            
            return APIResponse.success(
                {'message': '기술 정보가 성공적으로 삭제되었습니다.'}
            )
            
        except Technology.DoesNotExist:
            return APIResponse.error("기술 정보를 찾을 수 없습니다.", 404, "TECHNOLOGY_NOT_FOUND")
        except Exception as e:
            api_logger.error(f"기술 삭제 오류: {str(e)}")
            return APIResponse.error("서버 오류가 발생했습니다.", 500, "SERVER_ERROR")


class SearchAPIView(View):
    """통합 검색 API 뷰"""
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        """통합 검색"""
        try:
            query = request.GET.get('q', '')
            search_type = request.GET.get('type', 'all')  # all, notice, technology, client
            page = int(request.GET.get('page', 1))
            per_page = int(request.GET.get('per_page', 10))
            
            results = []
            
            if search_type in ['all', 'notice']:
                # 공지사항 검색
                notices = Notice.objects.filter(
                    Q(title__icontains=query) | Q(content__icontains=query)
                ).filter(status='published')[:10]
                
                for notice in notices:
                    results.append({
                        'type': 'notice',
                        'id': notice.id,
                        'title': notice.title,
                        'preview': notice.content[:100] + '...' if len(notice.content) > 100 else notice.content,
                        'url': f'/공지사항/{notice.id}/',
                        'date': notice.created_at.isoformat(),
                        'author': notice.author.username
                    })
            
            if search_type in ['all', 'technology']:
                # 기술 검색
                technologies = Technology.objects.filter(
                    Q(name__icontains=query) | 
                    Q(description__icontains=query) |
                    Q(tags__icontains=query)
                )[:10]
                
                for tech in technologies:
                    results.append({
                        'type': 'technology',
                        'id': tech.id,
                        'title': tech.name,
                        'preview': tech.description[:100] + '...' if len(tech.description) > 100 else tech.description,
                        'url': f'/기술/{tech.id}/',
                        'date': tech.created_at.isoformat(),
                        'author': tech.author.username,
                        'category': tech.get_category_display()
                    })
            
            if search_type in ['all', 'client']:
                # 거래처 검색
                clients = customer_information.objects.filter(
                    Q(company_name__icontains=query) |
                    Q(representative__icontains=query) |
                    Q(sectors__icontains=query)
                )[:10]
                
                for client in clients:
                    results.append({
                        'type': 'client',
                        'id': client.id,
                        'title': client.company_name,
                        'preview': f"대표자: {client.representative}, 업종: {client.sectors}",
                        'url': f'/client_inform/{client.id}/',
                        'date': client.registration_date.isoformat() if client.registration_date else '',
                        'region': client.region
                    })
            
            # 결과 정렬 (최신순)
            results.sort(key=lambda x: x['date'], reverse=True)
            
            return APIResponse.success({
                'query': query,
                'type': search_type,
                'results': results[:per_page],
                'total': len(results)
            })
            
        except Exception as e:
            api_logger.error(f"검색 오류: {str(e)}")
            return APIResponse.error("서버 오류가 발생했습니다.", 500, "SERVER_ERROR")


class StatsAPIView(View):
    """통계 API 뷰"""
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        """시스템 통계"""
        try:
            stats = {
                'notices': {
                    'total': Notice.objects.count(),
                    'published': Notice.objects.filter(status='published').count(),
                    'draft': Notice.objects.filter(status='draft').count(),
                    'urgent': Notice.objects.filter(importance='urgent').count(),
                    'this_month': Notice.objects.filter(
                        created_at__month=datetime.now().month,
                        created_at__year=datetime.now().year
                    ).count()
                },
                'technologies': {
                    'total': Technology.objects.count(),
                    'by_category': {},
                    'by_proficiency': {},
                    'by_status': {},
                    'this_month': Technology.objects.filter(
                        created_at__month=datetime.now().month,
                        created_at__year=datetime.now().year
                    ).count()
                },
                'clients': {
                    'total': customer_information.objects.count(),
                    'by_region': {},
                    'by_sector': {},
                    'active_contracts': customer_information.objects.filter(
                        contract_status='진행중'
                    ).count(),
                    'this_month': customer_information.objects.filter(
                        registration_date__month=datetime.now().month,
                        registration_date__year=datetime.now().year
                    ).count()
                }
            }
            
            # 기술 통계 계산
            for category, display in Technology.CATEGORY_CHOICES:
                stats['technologies']['by_category'][display] = Technology.objects.filter(category=category).count()
            
            for proficiency, display in Technology.PROFICIENCY_CHOICES:
                stats['technologies']['by_proficiency'][display] = Technology.objects.filter(proficiency=proficiency).count()
            
            for status, display in Technology.STATUS_CHOICES:
                stats['technologies']['by_status'][display] = Technology.objects.filter(status=status).count()
            
            # 거래처 통계 계산
            regions = customer_information.objects.values('region').distinct()
            for region in regions:
                stats['clients']['by_region'][region['region']] = customer_information.objects.filter(region=region['region']).count()
            
            sectors = customer_information.objects.values('sectors').distinct()
            for sector in sectors:
                stats['clients']['by_sector'][sector['sectors']] = customer_information.objects.filter(sectors=sector['sectors']).count()
            
            return APIResponse.success(stats)
            
        except Exception as e:
            api_logger.error(f"통계 조회 오류: {str(e)}")
            return APIResponse.error("서버 오류가 발생했습니다.", 500, "SERVER_ERROR")
