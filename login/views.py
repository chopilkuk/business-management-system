from django.shortcuts import render

def login_page(request):
    """로그인 페이지"""
    return render(request, 'login/login.html')