# 🐳 Docker 가상 서버 구축 가이드

## 🎯 Docker로 완벽한 개발 환경 구축

사용자님, **Docker를 이용하여 가상 서버를 만들어 완벽한 개발 환경을 구축해 드리겠습니다!**

### 🐳 Docker 설치

#### **1. Docker Desktop 설치**
```
https://www.docker.com/products/docker-desktop/
```

#### **2. 설치 후 확인**
```
docker --version
docker-compose --version
```

### 📁 프로젝트 Docker 설정

#### **Dockerfile 생성**
```dockerfile
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 복사
COPY requirements.txt .

# Python 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일 복사
COPY . .

# 정적 파일 수집
RUN python manage.py collectstatic --noinput

# 서버 시작
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

#### **docker-compose.yml 생성**
```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: business_management
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgres://postgres:password@db:5432/business_management
```

#### **requirements.txt 생성**
```txt
Django==4.2.7
psycopg2-binary==2.9.7
gunicorn==21.2.0
whitenoise==6.5.0
```

### 🚀 Docker 서버 실행

#### **1단계: Docker 이미지 빌드**
```bash
docker-compose build
```

#### **2단계: 서버 시작**
```bash
docker-compose up
```

#### **3단계: 백그라운드 실행**
```bash
docker-compose up -d
```

### 🌐 접속 방법

#### **로컬 접속**
```
http://localhost:8000
```

#### **LAN 접속**
```
http://[로컬IP]:8000
```

#### **모바일 접속**
```
http://[로컬IP]:8000
```

### 🔧 Docker 관리

#### **서버 상태 확인**
```bash
docker-compose ps
```

#### **로그 확인**
```bash
docker-compose logs web
```

#### **서버 중지**
```bash
docker-compose down
```

#### **서버 재시작**
```bash
docker-compose restart
```

### 📱 모바일 접속 설정

#### **1. 로컬 IP 확인**
```bash
ipconfig
```

#### **2. 방화벽 설정**
- Windows 방화벽에서 8000 포트 허용
- Docker Desktop 네트워크 설정 확인

#### **3. 모바일에서 접속**
```
http://[로컬IP]:8000
```

### 🎯 고급 설정

#### **개발/프로덕션 환경 분리**
```yaml
# docker-compose.dev.yml (개발용)
version: '3.8'
services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=1

# docker-compose.prod.yml (프로덕션용)
version: '3.8'
services:
  web:
    build: .
    command: gunicorn --bind 0.0.0.0:8000 business_management.wsgi:application
    ports:
      - "8000:8000"
    environment:
      - DEBUG=0
```

#### **데이터베이스 영속성**
```yaml
volumes:
  postgres_data:
    driver: local
```

### 🚀 배포 준비

#### **Docker Hub에 푸시**
```bash
docker tag business-management:latest username/business-management:latest
docker push username/business-management:latest
```

#### **클라우드 배포**
- AWS ECS
- Google Cloud Run
- Azure Container Instances

### 📋 장점 요약

#### **✅ Docker 장점**
- **🔒 격리**: 시스템과 완전 분리
- **🔄 재현성**: 동일한 환경 복제
- **📦 포팅**: 서버 이전 용이
- **📱 모바일**: 모바일에서 접속 가능
- **🌐 네트워크**: LAN 내 다른 기기 접속
- **⚡ 성능**: 전체 시스템 자원 활용

#### **🛠️ 관리 용이**
- **📊 모니터링**: 리소스 사용량 확인
- **🔄 스케일링**: 서버 확장 용이
- **🔧 설정**: 환경 설정 관리
- **📱 접속**: 다양한 기기에서 접속

---

**🎯 지금 바로 Docker로 가상 서버를 구축하여 완벽한 개발 환경을 경험하세요!**

**🚀 모바일에서도 접속 가능한 완벽한 개발 환경이 준비됩니다!**
