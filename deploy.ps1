# PowerShell 배포 스크립트
# 사용법: .\deploy.ps1 [환경] [옵션]

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("development", "staging", "production")]
    [string]$Environment = "production",
    
    [Parameter(Mandatory=$false)]
    [bool]$BackupDB = $true,
    
    [Parameter(Mandatory=$false)]
    [bool]$RunMigrations = $true,
    
    [Parameter(Mandatory=$false)]
    [bool]$CollectStatic = $true
)

# 색상 출력 함수
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# 환경 체크
function Check-Environment {
    Write-Info "배포 환경: $Environment"
    
    # 필수 파일 체크
    if (-not (Test-Path ".env.$Environment")) {
        Write-Error ".env.$Environment 파일이 없습니다."
        exit 1
    }
    
    if (-not (Test-Path "docker-compose.yml")) {
        Write-Error "docker-compose.yml 파일이 없습니다."
        exit 1
    }
    
    # Docker 확인
    try {
        docker --version > $null
        docker-compose --version > $null
    }
    catch {
        Write-Error "Docker 또는 docker-compose가 설치되지 않았습니다."
        exit 1
    }
}

# 데이터베이스 백업
function Backup-Database {
    if ($BackupDB) {
        Write-Info "데이터베이스 백업 중..."
        
        $backupDir = "backups"
        if (-not (Test-Path $backupDir)) {
            New-Item -ItemType Directory -Path $backupDir -Force
        }
        
        $backupFile = "$backupDir\backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').sql"
        
        try {
            docker-compose exec db pg_dump -U postgres business_management > $backupFile
            if ($LASTEXITCODE -eq 0) {
                Write-Success "데이터베이스 백업 완료: $backupFile"
            }
            else {
                Write-Error "데이터베이스 백업 실패"
                exit 1
            }
        }
        catch {
            Write-Error "데이터베이스 백업 중 오류 발생: $_"
            exit 1
        }
    }
}

# 환경 변수 설정
function Set-EnvironmentVariables {
    Write-Info "환경 변수 설정 중..."
    
    # .env 파일 복사
    Copy-Item ".env.$Environment" ".env" -Force
    
    Write-Success "환경 변수 설정 완료"
}

# Docker 이미지 빌드
function Build-Images {
    Write-Info "Docker 이미지 빌드 중..."
    
    try {
        docker-compose build --no-cache
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Docker 이미지 빌드 완료"
        }
        else {
            Write-Error "Docker 이미지 빌드 실패"
            exit 1
        }
    }
    catch {
        Write-Error "Docker 이미지 빌드 중 오류 발생: $_"
        exit 1
    }
}

# 컨테이너 시작
function Start-Containers {
    Write-Info "컨테이너 시작 중..."
    
    try {
        # 기존 컨테이너 중지
        docker-compose down
        
        # 컨테이너 시작
        docker-compose up -d
        
        # 헬스 체크 대기
        Write-Info "서비스 헬스 체크 대기 중..."
        Start-Sleep -Seconds 30
        
        # 서비스 상태 확인
        $containerStatus = docker-compose ps
        if ($containerStatus -match "Up") {
            Write-Success "컨테이너 시작 완료"
        }
        else {
            Write-Error "컨테이너 시작 실패"
            docker-compose logs
            exit 1
        }
    }
    catch {
        Write-Error "컨테이너 시작 중 오류 발생: $_"
        exit 1
    }
}

# 데이터베이스 마이그레이션
function Invoke-Migrations {
    if ($RunMigrations) {
        Write-Info "데이터베이스 마이그레이션 실행 중..."
        
        try {
            docker-compose exec web python manage.py migrate
            if ($LASTEXITCODE -eq 0) {
                Write-Success "마이그레이션 완료"
            }
            else {
                Write-Error "마이그레이션 실패"
                exit 1
            }
        }
        catch {
            Write-Error "마이그레이션 중 오류 발생: $_"
            exit 1
        }
    }
}

# 정적 파일 수집
function Collect-StaticFiles {
    if ($CollectStatic) {
        Write-Info "정적 파일 수집 중..."
        
        try {
            docker-compose exec web python manage.py collectstatic --noinput
            if ($LASTEXITCODE -eq 0) {
                Write-Success "정적 파일 수집 완료"
            }
            else {
                Write-Error "정적 파일 수집 실패"
                exit 1
            }
        }
        catch {
            Write-Error "정적 파일 수집 중 오류 발생: $_"
            exit 1
        }
    }
}

# 슈퍼유저 생성
function New-SuperUser {
    Write-Info "슈퍼유저 확인 중..."
    
    try {
        $superuserExists = docker-compose exec -T web python manage.py shell -c "
from django.contrib.auth.models import User
print(User.objects.filter(is_superuser=True).exists())
" 2>$null
        
        if ($superuserExists -eq "False") {
            Write-Warning "슈퍼유저가 없습니다. 생성이 필요합니다."
            $choice = Read-Host "슈퍼유저를 생성하시겠습니까? (y/n)"
            
            if ($choice -eq 'y' -or $choice -eq 'Y') {
                docker-compose exec web python manage.py createsuperuser
            }
        }
        else {
            Write-Success "슈퍼유저가 이미 존재합니다."
        }
    }
    catch {
        Write-Warning "슈퍼유저 확인 중 오류 발생: $_"
    }
}

# 헬스 체크
function Test-Health {
    Write-Info "최종 헬스 체크 중..."
    
    # 웹 서비스 체크
    try {
        $webHealth = Invoke-WebRequest -Uri "http://localhost:8000/health/" -UseBasicParsing -TimeoutSec 10
        if ($webHealth.Content -match "healthy") {
            Write-Success "웹 서비스 정상"
        }
        else {
            Write-Error "웹 서비스 비정상"
            exit 1
        }
    }
    catch {
        Write-Error "웹 서비스 헬스 체크 실패: $_"
        exit 1
    }
    
    # 데이터베이스 체크
    try {
        $dbHealth = docker-compose exec -T db pg_isready -U postgres
        if ($dbHealth -match "accepting connections") {
            Write-Success "데이터베이스 정상"
        }
        else {
            Write-Error "데이터베이스 비정상"
            exit 1
        }
    }
    catch {
        Write-Error "데이터베이스 헬스 체크 실패: $_"
        exit 1
    }
    
    # Redis 체크
    try {
        $redisHealth = docker-compose exec -T redis redis-cli ping
        if ($redisHealth -eq "PONG") {
            Write-Success "Redis 정상"
        }
        else {
            Write-Error "Redis 비정상"
            exit 1
        }
    }
    catch {
        Write-Error "Redis 헬스 체크 실패: $_"
        exit 1
    }
}

# 배포 후 작업
function Invoke-PostDeploy {
    Write-Info "배포 후 작업 실행 중..."
    
    # 캐시 워밍
    try {
        docker-compose exec web python manage.py warm_cache 2>$null
    }
    catch {
        Write-Warning "캐시 워밍 실패 (무시 가능)"
    }
    
    Write-Success "배포 후 작업 완료"
}

# 메인 함수
function Main {
    Write-Info "배포 시작: $Environment 환경"
    
    # 배포 단계 실행
    Check-Environment
    Backup-Database
    Set-EnvironmentVariables
    Build-Images
    Start-Containers
    Invoke-Migrations
    Collect-StaticFiles
    New-SuperUser
    Test-Health
    Invoke-PostDeploy
    
    Write-Success "배포 완료! 🎉"
    Write-Info "애플리케이션 URL: http://localhost:8000"
    
    # 운영 환경인 경우 HTTPS URL 안내
    if ($Environment -eq "production") {
        Write-Info "HTTPS URL: https://yourdomain.com"
    }
}

# 에러 핸들링
trap {
    Write-Error "배포 중 오류 발생! 롤백을 고려해주세요."
    exit 1
}

# 스크립트 실행
Main
