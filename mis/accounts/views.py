from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserLoginSerializer, UserWithProfileSerializer
from accounts.models import User
from accounts.permissions import IsAdminUser, IsDoctorUser, IsPatientUser


class LoginView(APIView):
    """Представление для аутентификации пользователя."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserWithProfileSerializer(user).data
        }, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    """Представление для получения данных профиля пользователя."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserWithProfileSerializer(user)
        return Response(serializer.data)


class AdminOnlyView(APIView):
    """Представление для доступа только для администраторов."""
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get(self, request):
        return Response({"message": "Только для администраторов"}, status=status.HTTP_200_OK)


class DoctorOnlyView(APIView):
    """Представление для доступа только для врачей."""
    permission_classes = [permissions.IsAuthenticated, IsDoctorUser]

    def get(self, request):
        return Response({"message": "Только для врачей"}, status=status.HTTP_200_OK)


class PatientOnlyView(APIView):
    """Представление для доступа только для пациентов."""
    permission_classes = [permissions.IsAuthenticated, IsPatientUser]

    def get(self, request):
        return Response({"message": "Только для пациентов"}, status=status.HTTP_200_OK)