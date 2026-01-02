from django.shortcuts import render

def commute_main(request):
    """근태 관리 메인 페이지"""
    return render(request, 'commute.html')