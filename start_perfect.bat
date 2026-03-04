@echo off
echo 비즈니스 관리 시스템 - 완벽 서버 시작
echo ======================================
echo.
echo 1. 시스템 점검 중...
echo    - 데이터베이스 마이그레이션 확인
echo    - 정적 파일 수집 확인
echo    - 서버 포트 확인
echo.

cd /d "%~dp0"

echo 2. 데이터베이스 마이그레이션 실행...
python manage.py migrate
echo.

echo 3. 정적 파일 수집...
python manage.py collectstatic --noinput --clear
echo.

echo 4. 기존 프로세스 정리...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 >nul

echo 5. 서버 시작 (모든 IP 허용)...
echo    서버 주소: http://127.0.0.1:8000/
echo    완성형: http://127.0.0.1:8000/complete/
echo    워크스페이스: http://127.0.0.1:8000/workspace/
echo.
python manage.py runserver 0.0.0.0:8000 --insecure --noreload
echo.
echo 6. 서버가 종료되었습니다.
echo ======================================
pause
