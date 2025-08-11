from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, UserProfileView, AdminOnlyView, DoctorOnlyView, PatientOnlyView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('admin-only/', AdminOnlyView.as_view(), name='admin_only'),
    path('doctor-only/', DoctorOnlyView.as_view(), name='doctor_only'),
    path('patient-only/', PatientOnlyView.as_view(), name='patient_only'),
]