from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """Кастомная проверка прав администратора."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()


class IsDoctorUser(permissions.BasePermission):
    """Кастомная проверка прав доктора."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_doctor()


class IsPatientUser(permissions.BasePermission):
    """Кастомная проверка прав пациента."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_patient()