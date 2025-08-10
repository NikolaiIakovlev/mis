from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, DoctorClinic

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'full_name', 'role', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('last_name', 'first_name')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Профессиональная информация', {
            'fields': ('role', 'specialization')
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Даты', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(DoctorClinic)
class DoctorClinicAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'clinic')
    list_filter = ('clinic',)
    search_fields = ('doctor__last_name', 'doctor__first_name', 'clinic__name')