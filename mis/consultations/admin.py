from django.contrib import admin
from .models import Consultation


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'doctor',
        'patient',
        'clinic',
        'start_time',
        'end_time',
        'status'
    )
    list_filter = ('status', 'clinic', 'start_time')
    search_fields = (
        'doctor__last_name',
        'doctor__first_name',
        'patient__last_name',
        'patient__first_name'
    )
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'start_time'
    list_per_page = 20
    
    fieldsets = (
        (None, {
            'fields': ('doctor', 'patient', 'clinic')
        }),
        ('Время консультации', {
            'fields': ('start_time', 'end_time')
        }),
        ('Статус', {
            'fields': ('status',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )