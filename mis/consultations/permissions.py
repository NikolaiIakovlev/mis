from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'doctor'

class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'patient'

class IsDoctorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['doctor', 'admin']

class IsPatientOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['patient', 'admin']