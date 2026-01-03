from django.shortcuts import render

def home(request):
    """홈 페이지 뷰"""
    return render(request, 'home/home.html')

def calendar(request):
    """캘린더 페이지 뷰"""
    return render(request, 'home/calendar.html')

def data(request):
    """자료 페이지 뷰"""
    return render(request, 'home/data.html')

def authority(request):
    """권한 페이지 뷰"""
    return render(request, 'home/authority.html')

def setting(request):
    """설정 페이지 뷰"""
    return render(request, 'home/setting.html')

def address(request):
    """주소록 페이지 뷰"""
    return render(request, 'home/address.html')
