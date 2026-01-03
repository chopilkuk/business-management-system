@echo off
echo Django 서버 시작 중...
echo.
echo 중요: 반드시 HTTP로 접속하세요!
echo 주소: http://127.0.0.1:8005
echo.
cd /d "c:\Users\Admin\Documents\협업\새 폴더"
python manage.py runserver 127.0.0.1:8005
pause
