from django.shortcuts import render

def index(request):
    """업무 상태 메인 페이지"""
    return render(request, 'businessStatus.html')
