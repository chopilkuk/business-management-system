@echo off
echo 비즈니스 관리 시스템 - 연결 문제 해결 서버
echo ==========================================
echo.
echo 1. 모든 포트 정리...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 >nul

echo 2. 새로운 서버 시작 (모든 IP 허용)...
cd /d "%~dp0"
python manage.py runserver 0.0.0.0:8000 --insecure --noreload
echo.
echo 3. 서버가 종료되었습니다.
echo ==========================================
echo.
echo 4. 브라우저에서 접속:
echo    http://127.0.0.1:8000/complete/
echo    http://localhost:8000/complete/
echo.
pause
