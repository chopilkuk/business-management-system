from django.shortcuts import render
from .models import Technology

def index(request):
    """기술 관리 메인 페이지 - 실제 기술 목록 표시"""
    technologies = Technology.objects.all().order_by('-created_at')
    return render(request, 'technology.html', {'technologies': technologies})
