from django.shortcuts import render

def home(request):
    """홈 페이지 뷰"""
    return render(request, 'home/home.html')
