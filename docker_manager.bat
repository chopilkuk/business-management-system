@echo off
title Docker 가상 서버 관리
color 0E
echo.
echo ========================================
echo    Docker 가상 서버 관리
echo ========================================
echo.
echo 1. Docker 서버 시작
echo 2. 서버 상태 확인
echo 3. 로그 확인
echo 4. 서버 중지
echo 5. 서버 재시작
echo 6. 이미지 빌드
echo 7. 네트워크 정보 확인
echo.
set /p choice="메뉴를 선택하세요 (1-7): "

if "%choice%"=="1" goto start
if "%choice%"=="2" goto status
if "%choice%"=="3" goto logs
if "%choice%"=="4" goto stop
if "%choice%"=="5" goto restart
if "%choice%"=="6" goto build
if "%choice%"=="7" goto network
goto end

:start
echo.
echo 🐳 Docker 서버를 시작합니다...
cd /d "c:\Users\Admin\Documents\협업\새 폴더"
docker-compose up
goto end

:status
echo.
echo 📊 서버 상태를 확인합니다...
cd /d "c:\Users\Admin\Documents\협업\새 폴더"
docker-compose ps
goto end

:logs
echo.
echo 📋 로그를 확인합니다...
cd /d "c:\Users\Admin\Documents\협업\새 폴더"
docker-compose logs -f
goto end

:stop
echo.
echo 🛑 Docker 서버를 중지합니다...
cd /d "c:\Users\Admin\Documents\협업\새 폴더"
docker-compose down
goto end

:restart
echo.
echo 🔄 Docker 서버를 재시작합니다...
cd /d "c:\Users\Admin\Documents\협업\새 폴더"
docker-compose restart
goto end

:build
echo.
echo 🔨 Docker 이미지를 빌드합니다...
cd /d "c:\Users\Admin\Documents\협업\새 폴더"
docker-compose build
goto end

:network
echo.
echo 🌐 네트워크 정보를 확인합니다...
ipconfig
echo.
echo 📱 모바일 접속 주소:
echo    http://[위에서 찾은 IPv4 주소]:8000
goto end

:end
echo.
pause
