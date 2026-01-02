#!/bin/bash

# 배포 스크립트
# 사용법: ./deploy.sh [환경] [옵션]

set -e

# 기본 설정
ENVIRONMENT=${1:-production}
BACKUP_DB=${2:-true}
RUN_MIGRATIONS=${3:-true}
COLLECT_STATIC=${4:-true}

# 색상 출력 함수
print_info() {
    echo -e "\033[34m[INFO] $1\033[0m"
}

print_success() {
    echo -e "\033[32m[SUCCESS] $1\033[0m"
}

print_warning() {
    echo -e "\033[33m[WARNING] $1\033[0m"
}

print_error() {
    echo -e "\033[31m[ERROR] $1\033[0m"
}

# 환경 체크
check_environment() {
    print_info "배포 환경: $ENVIRONMENT"
    
    if [[ "$ENVIRONMENT" != "development" && "$ENVIRONMENT" != "staging" && "$ENVIRONMENT" != "production" ]]; then
        print_error "잘못된 환경입니다. (development|staging|production)"
        exit 1
    fi
    
    # 필수 파일 체크
    if [[ ! -f ".env.$ENVIRONMENT" ]]; then
        print_error ".env.$ENVIRONMENT 파일이 없습니다."
        exit 1
    fi
    
    if [[ ! -f "docker-compose.yml" ]]; then
        print_error "docker-compose.yml 파일이 없습니다."
        exit 1
    fi
}

# 데이터베이스 백업
backup_database() {
    if [[ "$BACKUP_DB" == "true" ]]; then
        print_info "데이터베이스 백업 중..."
        
        BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
        
        docker-compose exec db pg_dump -U postgres business_management > "./backups/$BACKUP_FILE"
        
        if [[ $? -eq 0 ]]; then
            print_success "데이터베이스 백업 완료: $BACKUP_FILE"
        else
            print_error "데이터베이스 백업 실패"
            exit 1
        fi
    fi
}

# 환경 변수 설정
setup_environment() {
    print_info "환경 변수 설정 중..."
    
    # .env 파일 복사
    cp ".env.$ENVIRONMENT" .env
    
    # 환경 변수 로드
    source .env
    
    print_success "환경 변수 설정 완료"
}

# Docker 이미지 빌드
build_images() {
    print_info "Docker 이미지 빌드 중..."
    
    docker-compose build --no-cache
    
    if [[ $? -eq 0 ]]; then
        print_success "Docker 이미지 빌드 완료"
    else
        print_error "Docker 이미지 빌드 실패"
        exit 1
    fi
}

# 컨테이너 시작
start_containers() {
    print_info "컨테이너 시작 중..."
    
    # 기존 컨테이너 중지
    docker-compose down
    
    # 컨테이너 시작
    docker-compose up -d
    
    # 헬스 체크 대기
    print_info "서비스 헬스 체크 대기 중..."
    sleep 30
    
    # 서비스 상태 확인
    if docker-compose ps | grep -q "Up"; then
        print_success "컨테이너 시작 완료"
    else
        print_error "컨테이너 시작 실패"
        docker-compose logs
        exit 1
    fi
}

# 데이터베이스 마이그레이션
run_migrations() {
    if [[ "$RUN_MIGRATIONS" == "true" ]]; then
        print_info "데이터베이스 마이그레이션 실행 중..."
        
        docker-compose exec web python manage.py migrate
        
        if [[ $? -eq 0 ]]; then
            print_success "마이그레이션 완료"
        else
            print_error "마이그레이션 실패"
            exit 1
        fi
    fi
}

# 정적 파일 수집
collect_static() {
    if [[ "$COLLECT_STATIC" == "true" ]]; then
        print_info "정적 파일 수집 중..."
        
        docker-compose exec web python manage.py collectstatic --noinput
        
        if [[ $? -eq 0 ]]; then
            print_success "정적 파일 수집 완료"
        else
            print_error "정적 파일 수집 실패"
            exit 1
        fi
    fi
}

# 슈퍼유저 생성
create_superuser() {
    print_info "슈퍼유저 확인 중..."
    
    # 슈퍼유저가 있는지 확인
    SUPERUSER_EXISTS=$(docker-compose exec -T web python manage.py shell -c "
from django.contrib.auth.models import User
print(User.objects.filter(is_superuser=True).exists())
" 2>/dev/null || echo "False")
    
    if [[ "$SUPERUSER_EXISTS" == "False" ]]; then
        print_warning "슈퍼유저가 없습니다. 생성이 필요합니다."
        read -p "슈퍼유저를 생성하시겠습니까? (y/n): " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker-compose exec web python manage.py createsuperuser
        fi
    else
        print_success "슈퍼유저가 이미 존재합니다."
    fi
}

# 헬스 체크
health_check() {
    print_info "최종 헬스 체크 중..."
    
    # 웹 서비스 체크
    WEB_HEALTH=$(curl -f -s http://localhost:8000/health/ || echo "failed")
    
    if [[ "$WEB_HEALTH" == "healthy" ]]; then
        print_success "웹 서비스 정상"
    else
        print_error "웹 서비스 비정상"
        exit 1
    fi
    
    # 데이터베이스 체크
    DB_HEALTH=$(docker-compose exec -T db pg_isready -U postgres || echo "failed")
    
    if [[ "$DB_HEALTH" == *"accepting connections"* ]]; then
        print_success "데이터베이스 정상"
    else
        print_error "데이터베이스 비정상"
        exit 1
    fi
    
    # Redis 체크
    REDIS_HEALTH=$(docker-compose exec -T redis redis-cli ping || echo "failed")
    
    if [[ "$REDIS_HEALTH" == "PONG" ]]; then
        print_success "Redis 정상"
    else
        print_error "Redis 비정상"
        exit 1
    fi
}

# 배포 후 작업
post_deploy() {
    print_info "배포 후 작업 실행 중..."
    
    # 캐시 워밍
    docker-compose exec web python manage.py warm_cache || true
    
    # 로그 로테이트
    docker-compose exec web python manage.py rotate_logs || true
    
    print_success "배포 후 작업 완료"
}

# 롤백 함수
rollback() {
    print_warning "롤백 시작..."
    
    # 이전 버전으로 롤백
    docker-compose down
    docker-compose up -d
    
    print_info "롤백 완료"
}

# 메인 함수
main() {
    print_info "배포 시작: $ENVIRONMENT 환경"
    
    # 백업 디렉토리 생성
    mkdir -p backups
    
    # 배포 단계 실행
    check_environment
    backup_database
    setup_environment
    build_images
    start_containers
    run_migrations
    collect_static
    create_superuser
    health_check
    post_deploy
    
    print_success "배포 완료! 🎉"
    print_info "애플리케이션 URL: http://localhost:8000"
    
    # 운영 환경인 경우 HTTPS URL 안내
    if [[ "$ENVIRONMENT" == "production" ]]; then
        print_info "HTTPS URL: https://yourdomain.com"
    fi
}

# 에러 핸들링
trap 'print_error "배포 중 오류 발생! 롤백을 고려해주세요."' ERR

# 스크립트 실행
main "$@"
