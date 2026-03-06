@echo off
echo 비즈니스 관리 시스템 - 완성형 서버 시작
echo =========================================
echo.
echo 1. SSL 오류 방지 서버 시작 중...
cd /d "%~dp0"
python manage.py runserver 127.0.0.1:8000 --insecure --noreload
echo.
echo 2. 서버가 종료되었습니다.
echo =========================================
echo.
echo 3. 브라우저에서 접속:
echo    http://127.0.0.1:8000/complete/
echo.
pause
