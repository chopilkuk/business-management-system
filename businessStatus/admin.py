from django.contrib import admin
from .models import BusinessStatus

@admin.register(BusinessStatus)
class BusinessStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
