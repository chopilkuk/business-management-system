# 릴리스 체크리스트

1. 모든 테스트 통과
2. 린트(black/isort/flake8) 통과
3. 마이그레이션 생성 및 적용 확인
4. `README.md`에 변경 로그 추가
5. 태그 생성: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
6. 배포 전 `collectstatic --noinput` 실행
7. 환경변수(SECRET_KEY, DATABASE 등) 확인
8. 모니터링(Sentry) 및 로그 설정 확인
