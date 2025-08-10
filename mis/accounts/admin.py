from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Doctor, Patient

# Настройки для User
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Права доступа', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role'),
        }),
    )


# Настройки для Doctor
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialization', 'user', 'clinics_list')
    list_select_related = ('user',)
    search_fields = ('last_name', 'first_name', 'middle_name', 'specialization')
    list_filter = ('specialization', 'clinics')
    filter_horizontal = ('clinics',)
    readonly_fields = ('user_link',)
    fieldsets = (
        (None, {
            'fields': ('user_link', 'last_name', 'first_name', 'middle_name')
        }),
        ('Профессиональная информация', {
            'fields': ('specialization', 'clinics')
        }),
    )

    def user_link(self, obj):
        if obj.user:
            return admin.utils.lookup_field('username', obj.user, DoctorAdmin)[2]
        return "-"
    user_link.short_description = "Пользователь"

    def clinics_list(self, obj):
        return ", ".join([c.name for c in obj.clinics.all()])
    clinics_list.short_description = "Клиники"


# Настройки для Patient
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phonenumber', 'email', 'user_link')
    search_fields = ('last_name', 'first_name', 'middle_name', 'phonenumber', 'email')
    readonly_fields = ('user_link',)
    fieldsets = (
        (None, {
            'fields': ('user_link', 'last_name', 'first_name', 'middle_name')
        }),
        ('Контактная информация', {
            'fields': ('phonenumber', 'email')
        }),
    )

    def user_link(self, obj):
        if obj.user:
            return admin.utils.lookup_field('username', obj.user, PatientAdmin)[2]
        return "-"
    user_link.short_description = "Пользователь"
