# 비즈니스 관리 시스템

🏢 완벽한 비즈니스 관리 시스템입니다.

## 🌟 주요 기능

- 🌍 글로벌 내비게이션 바
- 📱 반응형 디자인
- 🔍 실시간 검색
- 🔔 알림 시스템
- 👤 사용자 관리
- 📊 대시보드
- 📢 공지사항 관리
- 🏢 거래처 정보 관리
- ⏰ 근태 관리
- 📈 업무 상태 관리
- 🔧 기술 관리
- 🔐 보안 강화

## 🚀 기술 스택

- **Backend**: Django 6.0
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite
- **UI**: Bootstrap, FontAwesome
- **Real-time**: WebSocket, AJAX

## 🎯 설치 및 실행

### 로컬 실행
```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install django

# 데이터베이스 마이그레이션
python manage.py migrate

# 서버 실행
python manage.py runserver
```

### 접속
- **로컬**: http://127.0.0.1:8000
- **GitHub Pages**: (배포 후 주소)

## 🌐 배포

### GitHub Pages로 배포
1. 이 저장소를 Fork합니다
2. GitHub Pages 설정에서 소스를 `main` 브랜치로 설정
3. 몇 분 후 사이트가 배포됩니다

### Heroku로 배포
```bash
# Heroku CLI 설치 후
heroku create
git push heroku main
```

## 📱 주요 페이지

- 🏠 **홈**: 대시보드 및 네비게이션
- 📢 **공지사항**: CRUD 기능
- 🏢 **거래처 정보**: 관리 시스템
- ⏰ **근태 관리**: 출퇴근 시스템
- 📊 **업무 상태**: 통계 및 차트
- 🔧 **기술 관리**: 연구소 시스템

## 🔐 보안 기능

- SQL 인젝션 방지
- XSS 방어
- CSRF 보호
- 입력 데이터 검증
- 권한 관리

## 🎨 UI/UX

- 🌙 다크 모드 지원
- 📱 모바일 반응형
- 🎨 현대적 디자인
- ⚡ 부드러운 애니메이션
- 🔍 실시간 검색

## 📞 문의

개발자: Cascade AI Assistant
이메일: support@business-management.com

## 📄 라이선스

MIT License
- 할당된 작업 관리
- 진행 상황 모니터링

### 🔔 알림 시스템
- 실시간 알림
- 우선 알림 필터링
- 알림 이력 관리

### 👥 사용자 관리
- 로그인/회원가입
- 권한 관리
- 프로필 설정

## 🛠️ 기술 스택

- **Backend**: Django 4.2.7
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Database**: SQLite (개발), PostgreSQL (운영)
- **Security**: CSRF 보호, XSS 방지, 입력값 검증
- **Styling**: Modern CSS with CSS Variables
- **Deployment**: Gunicorn + Nginx

## 📦 설치 및 설정

### 1. 가상환경 생성
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 데이터베이스 설정
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 슈퍼유저 생성
```bash
python manage.py createsuperuser
```

### 5. 정적 파일 수집
```bash
python manage.py collectstatic
```

### 6. 서버 실행
```bash
python manage.py runserver
```

## 🔧 설정

### 환경 변수
`.env` 파일을 생성하고 다음 변수들을 설정하세요:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### 데이터베이스 설정
운영 환경에서는 PostgreSQL 사용을 권장합니다:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'business_management',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📁 프로젝트 구조

```
business_management/
├── business_management/          # 메인 프로젝트 설정
│   ├── settings.py              # Django 설정
│   ├── urls.py                  # URL 라우팅
│   ├── middleware.py            # 보안 미들웨어
│   ├── validators.py            # 데이터 검증
│   ├── exceptions.py            # 사용자 정의 예외
│   ├── error_handlers.py        # 에러 핸들링
│   └── utils.py                 # 유틸리티 함수
├── client_inform/               # 거래처 관리 앱
├── commute/                     # 근태 관리 앱
├── home/                        # 홈페이지 앱
├── login/                       # 로그인 앱
├── static/                      # 정적 파일
│   ├── css/                     # CSS 파일
│   ├── js/                      # JavaScript 파일
│   └── images/                  # 이미지 파일
├── templates/                   # 템플릿 파일
├── media/                       # 미디어 파일
├── requirements.txt             # 의존성 목록
└── README.md                    # 프로젝트 문서
```

## 🔒 보안 기능

### 보안 미들웨어
- **SecurityHeadersMiddleware**: 보안 헤더 추가
- **RateLimitMiddleware**: 요청 속도 제한
- **SecurityLoggingMiddleware**: 보안 이벤트 로깅
- **InputValidationMiddleware**: 입력값 검증

### 데이터 검증
- 사업자등록번호 체크섬 검증
- 이메일 형식 검증
- 전화번호 형식 검증
- XSS 방지 입력값 정제

### 인증 및 권한
- Django 기본 인증 시스템
- CSRF 보호
- 세션 보안
- 비밀번호 강도 검증

## 🧪 테스트

### 테스트 실행
```bash
python manage.py test
```

### 테스트 커버리지
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 📝 API 문서

### 거래처 관리 API
- `GET /client_inform/` - 거래처 목록 조회
- `POST /client_inform/api/add/` - 거래처 추가
- `PUT /client_inform/api/update/<id>/` - 거래처 수정
- `DELETE /client_inform/api/delete/` - 거래처 삭제
- `GET /client_inform/search/` - 거래처 검색

### 근태 관리 API
- `POST /commute/api/check-in/` - 출근 처리
- `POST /commute/api/check-out/` - 퇴근 처리
- `GET /commute/api/history/` - 근태 기록 조회
- `GET /commute/api/stats/` - 근태 통계

### 인증 API
- `POST /login/api/login/` - 로그인
- `POST /login/api/logout/` - 로그아웃
- `POST /login/api/find-id/` - 아이디 찾기
- `POST /login/api/reset-password/` - 비밀번호 재설정

## 🚀 배포

### Production 배포
1. **환경 변수 설정**
   ```env
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   ALLOWED_HOSTS=yourdomain.com
   ```

2. **정적 파일 수집**
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Gunicorn으로 실행**
   ```bash
   gunicorn business_management.wsgi:application --bind 0.0.0.0:8000
   ```

### Docker 배포
```bash
docker build -t business-management .
docker run -p 8000:8000 business-management
```

## 🐛 오류 처리

### 에러 로깅
- 모든 에러는 상세하게 로깅됩니다
- 개발 환경에서는 디버그 정보 제공
- 운영 환경에서는 일반적인 에러 메시지만 표시

### 모니터링
- Sentry 연동 지원
- 성능 모니터링
- 보안 이벤트 추적

## 🤝 기여

1. Fork 프로젝트
2. 기능 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. 커밋 (`git commit -m 'Add some AmazingFeature'`)
4. 푸시 (`git push origin feature/AmazingFeature`)
5. Pull Request 생성

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 지원

문제가 발생하거나 질문이 있으시면 다음 방법으로 연락주세요:

- 이슈 생성: [GitHub Issues](https://github.com/your-repo/issues)
- 이메일: support@yourcompany.com

## 🔄 변경 로그

### v1.0.0 (2024-01-15)
- 초기 릴리스
- 기본 기능 구현
- 보안 강화
- UI/UX 개선

---

**개발팀**: Your Company Development Team  
**최종 업데이트**: 2024-01-15
