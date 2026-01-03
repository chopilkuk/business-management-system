@echo off
title 비즈니스 관리 시스템 - 로컬 서버
color 0A
echo.
echo ========================================
echo    비즈니스 관리 시스템 로컬 서버
echo ========================================
echo.
echo 🚀 Django 개발 서버를 시작합니다...
echo.
echo 📍 접속 주소:
echo    http://127.0.0.1:8007
echo.
echo 🎯 실시간 개발 환경:
echo    - 코드 변경 즉시 반영
echo    - 자동 리로드 기능
echo    - 모든 기능 작동
echo.
echo 📱 모든 페이지:
echo    - 홈: http://127.0.0.1:8007/
echo    - 캘린더: http://127.0.0.1:8007/calendar/
echo    - 자료실: http://127.0.0.1:8007/data/
echo    - 권한 관리: http://127.0.0.1:8007/authority/
echo    - 설정: http://127.0.0.1:8007/setting/
echo    - 주소록: http://127.0.0.1:8007/address/
echo.
echo 🔧 서버 중지: Ctrl+C
echo ========================================
echo.
cd /d "c:\Users\Admin\Documents\협업\새 폴더"
python manage.py runserver 127.0.0.1:8007 --insecure
echo.
echo 서버가 중지되었습니다.
pause
