@echo off
title 비즈니스 관리 시스템 - Docker 가상 서버
color 0B
echo.
echo ========================================
echo    Docker 가상 서버 시작
echo ========================================
echo.
echo 🐳 Docker 컨테이너를 시작합니다...
echo.
echo 📍 접속 주소:
echo    http://localhost:8000
echo.
echo 🌐 네트워크 접속:
echo    http://[로컬IP]:8000
echo.
echo 📱 모바일 접속:
echo    http://[로컬IP]:8000
echo.
echo 🎯 가상 서버 장점:
echo    - 완벽한 격리 환경
echo    - 모바일 접속 가능
echo    - LAN 내 다른 기기 접속
echo    - 데이터 영속성 보장
echo.
echo 🔧 관리 명령어:
echo    - 상태 확인: docker-compose ps
echo    - 로그 확인: docker-compose logs
echo    - 중지: docker-compose down
echo.
echo 🚀 서버 중지: Ctrl+C
echo ========================================
echo.
cd /d "c:\Users\Admin\Documents\협업\새 폴더"
docker-compose up
echo.
echo Docker 서버가 중지되었습니다.
pause
