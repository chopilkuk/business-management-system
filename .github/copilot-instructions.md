# Copilot / AI 작업 지침 (요약)

이 파일은 이 레포에서 AI 코딩 에이전트가 빠르게 생산적일 수 있도록 핵심 컨텍스트와 규칙을 요약합니다.

1) 목적
- 이 프로젝트는 Django 기반의 내부 비즈니스 관리 시스템입니다. 빠른 로컬 개발, Docker 배포, 그리고 k8s 매니페스트가 포함되어 있습니다.

2) 아키텍처(한눈 요약)
- 프로젝트 루트: `manage.py`, `requirements.txt`, `Dockerfile`, `docker-compose.yml`, `k8s/`
- Django 프로젝트: `business_management/` — 설정(`settings.py`), URL(`urls.py`), WSGI/ASGI 등
- 주요 앱: `client_inform/`, `commute/`, `home/`, `login/`, `businessStatus/` 등 (각 앱에 `urls.py`, `views.py`, `models.py` 존재)
- 정적/템플릿: 전역 `static/`, 앱별 `static/`, 전역 `templates/` 및 앱 `templates/`
- 배포: Dockerfile + `gunicorn` + Nginx 조합, `k8s/`에 매니페스트 존재

3) 핵심 실행 / 개발 커맨드
- 의존성: `pip install -r requirements.txt`
- 마이그레이션: `python manage.py migrate`
- 개발서버: `python manage.py runserver`
- 테스트: `python manage.py test`
- 정적파일 수집(배포): `python manage.py collectstatic --noinput`
- Docker: `docker build -t business-management .` 및 `docker run -p 8000:8000 business-management`

4) 프로젝트 특이사항 및 규칙
- README에 Django 버전 표기가 일관되지 않습니다 (4.2.7 / 6.0). 실제 버전은 `requirements.txt`와 `business_management/settings.py`를 우선 확인하세요.
- DB: 개발은 SQLite, 운영은 PostgreSQL 권장 — 환경 변수는 `.env` 또는 시스템 env로 설정됩니다.
- URL 패턴: 각 앱이 자체 `urls.py`를 가지고 있으며 중앙 라우팅은 `business_management/urls.py`에서 포함합니다. 예: `client_inform/urls.py`를 찾아 패턴을 이어 붙이세요.
- 정적/템플릿 패턴: 앱 단위로 `templates/<app_name>/` 또는 전역 `templates/`를 사용합니다. 프론트는 순수 HTML/JS/CSS입니다 — 빌드 단계 없음.
- 미들웨어/유틸: 보안 관련 로직은 `business_management/` 내부(예: custom middleware, validators)에서 구현되어 있으니 변경 시 영향 범위 확인 필요.
- 한글 디렉터리: 일부 폴더/파일명이 한글(예: `공지사항/`, `기술/`)이므로 파일 경로 조작 시 유니코드 대응 유의.

5) 통합 포인트 / 외부 의존성
- 실시간 기능: WebSocket / AJAX 사용. 관련 뷰는 각 앱의 `views.py`와 `static/*.js`에 분산되어 있습니다.
- 모니터링/로깅: Sentry 연동 가능성이 언급되어 있으며, 에러 로깅 파일/미들웨어를 확인하세요.
- 배포: `Dockerfile`, `docker-compose.yml`, `k8s/` 매니페스트가 존재합니다. 프로덕션은 Gunicorn+Nginx 조합을 가정.

6) 코드 변경 시 체크리스트 (AI가 자동 변경할 때 따를 것)
- `manage.py`와 `business_management/settings.py` 변경 전에는 `requirements.txt`와 README의 버전 불일치 확인.
- 데이터베이스 스키마 변경이면 반드시 `makemigrations` + `migrate` 순으로 처리하고 테스트 실행.
- 정적 파일이나 템플릿 변경 시 `collectstatic` 필요 여부를 명시적으로 코멘트로 남길 것.
- 신규 URL 추가 시 `business_management/urls.py`에 include 확인.

7) 예시 참조 (빠른 탐색 포인트)
- 프로젝트 설정: `business_management/settings.py`
- 라우팅 진입점: `business_management/urls.py`, 앱 라우트 예시: `client_inform/urls.py`
- 실행 스크립트: `manage.py`
- 배포: `Dockerfile`, `docker-compose.yml`, `k8s/deployment.yaml`
- 요구사항: `requirements.txt`

8) 제한 및 금지된 작업
- 권한/인증 로직(예: 로그인, 권한 체크)에 대한 자동 리팩터는 피하고, 변경 제안 시 사람 리뷰를 필수로 요구하세요.
- 사용자 비밀번호, 시크릿키 등을 코드에 하드코딩하지 말 것.

9) 문의 및 반복
- 불확실한 의사결정(예: Django 버전 업그레이드, DB 마이그레이션 전략)은 PR로 제안하고 리뷰를 요청하세요.

---
피드백: 이 파일에 부족한 내용(특히 작업 흐름이나 CI 명령)이 있으면 알려주세요. 바로 수정하거나 확장하겠습니다.
