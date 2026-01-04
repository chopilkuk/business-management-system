**Production static deployment notes**

요약
- 배포 환경에서 정적 파일은 웹서버(Nginx) 또는 CDN이 직접 서빙하도록 구성합니다. Django `collectstatic`으로 파일을 모아 프로덕션 `STATIC_ROOT`에 배치한 뒤, 웹서버가 그 디렉터리를 서비스하도록 합니다.

1) Django 설정
- `settings.py`:
  - `STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')` (또는 절대 경로)
  - `STATIC_URL = '/static/'`
  - 프로덕션에서는 `DEBUG = False`로 설정

2) 정적 파일 수집
- 배포 서버에서(또는 CI):
  - `python manage.py collectstatic --noinput`

3) Nginx 예시 (정적 파일 서빙)
- 기본적인 location 설정:
  server {
    listen 80;
    server_name example.com;

    location /static/ {
      alias /path/to/your/project/staticfiles/;
      access_log off;
      expires 30d;
      add_header Cache-Control "public, max-age=2592000";
    }

    location / {
      proxy_pass http://127.0.0.1:8000;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
  }

4) WhiteNoise 대안
- 간단한 배포(예: Heroku)에서는 `whitenoise`를 사용해 Django에서 직접 정적 파일을 서빙할 수 있습니다. 설정 예시는 `whitenoise` 문서를 참고하세요.

5) 캐시와 파일 무효화
- 파일 이름에 해시를 붙이거나(예: `ManifestStaticFilesStorage`) CDN을 사용하는 것이 권장됩니다. 파일 변경 시 CDN 캐시 무효화 전략을 마련하세요.

6) 파일 충돌/중복 처리
- 프로젝트에 동일한 `static/<path>`가 여러 앱에 존재하면 `collectstatic`은 첫 발견 파일만 복사합니다. 충돌을 피하려면 파일 경로를 표준화하거나 앱 레벨 파일명을 변경하세요. `scripts/organize_static.py`는 앱의 `static/menu/`를 프로젝트 `static/menu/`로 복사해 병합을 돕습니다(비파괴적).

7) CI/CD 권장 흐름
- 빌드 단계: `pip install -r requirements.txt` → `python manage.py collectstatic --noinput` → 빌드 아티팩트(정적 파일)를 이미지 또는 CDN으로 업로드 → 배포.

8) 점검 목록
- `STATIC_ROOT`가 올바른지 확인
- Nginx `alias` 경로와 권한 확인
- 캐싱 헤더(Expires, Cache-Control) 설정 확인
- `SECRET_KEY`, DB 자격증명 등 민감정보는 환경변수로 관리
