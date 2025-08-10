from django.contrib import admin
from .models import Clinic


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'legal_address', 'physical_address')
    search_fields = ('name', 'legal_address', 'physical_address')
    list_per_page = 20
