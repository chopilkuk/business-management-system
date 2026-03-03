요약
-
이 프로젝트 로컬 개발 환경을 설정하는 최소한의 의존성 설치 가이드입니다.

Python 가상환경(권장)
- Python 3.10+ 설치를 권장합니다.
- 가상환경 생성 및 활성화:
  - `python -m venv .venv`
  - `source .venv/bin/activate`

파이썬 패키지 설치
- 시스템 의존성(우분투 예시):
  - `sudo apt update && sudo apt install -y build-essential libpq-dev python3-dev libjpeg-dev zlib1g-dev` 
- 파이썬 패키지 설치:
  - `pip install --upgrade pip`
  - `pip install -r requirements.txt`

데이터베이스 및 마이그레이션
- 개발은 SQLite 기본으로 동작합니다. 마이그레이션 적용:
  - `python manage.py migrate`

정적파일 수집(배포 시)
- 배포용으로 정적 파일을 모을 때:
  - `python manage.py collectstatic --noinput`

개발서버 실행
- 로컬 개발서버:
  - `python manage.py runserver`

추가 팁
- 일부 패키지(예: numpy, Pillow)는 시스템 라이브러리를 요구할 수 있습니다. 오류 발생 시 위의 시스템 의존성을 확인하세요.
- 배포 환경에서는 `SECRET_KEY`, DB 접속 정보 등을 환경 변수로 설정하세요.
