from django.contrib import admin
from .models import Doctor, Patient

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'specialization')
    search_fields = ('last_name', 'first_name', 'specialization')
    list_filter = ('specialization',)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'phonenumber', 'email')
    search_fields = ('last_name', 'first_name', 'phonenumber', 'email')


