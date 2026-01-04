# 기여 가이드

개발자 로컬에서 일관된 포맷과 검사를 실행하려면 다음을 따르세요.

1. 가상환경 생성
```bash
python -m venv venv
source venv/bin/activate
```

2. 의존성 설치
```bash
pip install -r requirements.txt
```

3. pre-commit 설치 및 훅 등록
```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

4. 코드 포맷(필수)
```bash
black .
isort .
```

5. 테스트 실행
```bash
python manage.py test
```

6. 변경사항 커밋
```bash
git checkout -b feature/your-feature
git add .
git commit -m "feat: 설명"
git push origin feature/your-feature
```
