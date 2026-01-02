from django.shortcuts import render
from .models import customer_information

def index(request):
    """거래처 관리 메인 페이지 - 실제 거래처 목록 표시"""
    clients = customer_information.objects.all().order_by('-registration_date')
    return render(request, 'client_inform.html', {'clients': clients})
