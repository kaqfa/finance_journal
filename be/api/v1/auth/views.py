# from django.contrib.auth.models import User
from master.models import User
from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    PasswordChangeSerializer,
    PasswordResetSerializer,
    RegTokenValidationSerializer
)


class RegisterView(generics.CreateAPIView):
    """
    Enhanced User Registration dengan Registration Token validation
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Override create untuk custom response dengan token info
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = serializer.save()
            
            # Generate JWT tokens untuk auto-login setelah register
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "message": "Registrasi berhasil! Selamat datang di Journal Invest.",
                "user": UserSerializer(user).data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                "error": "Registrasi gagal. Silakan coba lagi.",
                "details": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def validate_registration_token(request):
    """
    Endpoint untuk validasi registration token sebelum registrasi
    
    POST /api/v1/auth/validate-token/
    {
        "token_code": "ALPHA2025"
    }
    """
    serializer = RegTokenValidationSerializer(data=request.data)
    
    if serializer.is_valid():
        return Response(serializer.to_representation(None))
    
    return Response({
        "error": "Token tidak valid",
        "details": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Enhanced Login dengan informasi registration token
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        if not username or not password:
            return Response(
                {"error": "Username dan password wajib diisi"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if not user:
            return Response(
                {"error": "Username atau password salah"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active:
            return Response(
                {"error": "Akun tidak aktif. Hubungi administrator."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "message": f"Selamat datang kembali, {user.full_name or user.username}!",
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            },
            "user": UserSerializer(user).data
        })


class LogoutView(APIView):
    """
    Logout dengan blacklist token
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token diperlukan untuk logout"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({
                "message": "Logout berhasil. Sampai jumpa!"
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": "Logout gagal",
                "details": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    """
    Change password untuk authenticated user
    """
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            
            # Check old password
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {"old_password": ["Password lama salah."]}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({
                "message": "Password berhasil diubah."
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    """
    Password reset request (placeholder for email implementation)
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            # Check if user exists
            try:
                user = User.objects.get(email=email)
                
                # In a real implementation, send password reset email here
                # For now, we'll just return a success message
                
                return Response({
                    "message": "Email reset password telah dikirim ke alamat email Anda."
                }, status=status.HTTP_200_OK)
                
            except User.DoesNotExist:
                # Don't reveal that the user doesn't exist for security
                return Response({
                    "message": "Email reset password telah dikirim ke alamat email Anda."
                }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    User profile view dengan registration token info
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        """
        Override update untuk custom response
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Prevent updating sensitive fields
        protected_fields = ['username', 'reg_token', 'is_staff', 'is_superuser']
        for field in protected_fields:
            if field in serializer.validated_data:
                serializer.validated_data.pop(field)
        
        self.perform_update(serializer)
        
        return Response({
            "message": "Profile berhasil diupdate.",
            "user": serializer.data
        })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def registration_info(request):
    """
    Endpoint untuk mendapatkan informasi registrasi (apakah membutuhkan token, dll)
    
    GET /api/v1/auth/registration-info/
    """
    return Response({
        "requires_token": True,
        "message": "Registrasi membutuhkan token khusus. Hubungi administrator untuk mendapatkan token registrasi.",
        "steps": [
            "1. Dapatkan token registrasi dari administrator",
            "2. Validasi token menggunakan endpoint /auth/validate-token/",
            "3. Gunakan token untuk registrasi di endpoint /auth/register/"
        ]
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
def token_statistics(request):
    """
    Endpoint untuk admin mendapatkan statistik registration token
    
    GET /api/v1/auth/token-stats/
    """
    from master.models import RegToken
    from django.db.models import Count, Sum
    
    # Get token statistics
    tokens = RegToken.objects.all()
    active_tokens = tokens.filter(is_active=True)
    expired_tokens = tokens.filter(expires_at__lt=timezone.now())
    
    # User statistics
    users_with_tokens = User.objects.exclude(reg_token__isnull=True)
    
    stats = {
        "token_statistics": {
            "total_tokens": tokens.count(),
            "active_tokens": active_tokens.count(),
            "expired_tokens": expired_tokens.count(),
            "total_usage": tokens.aggregate(total=Sum('current_usage'))['total'] or 0
        },
        "user_statistics": {
            "total_users": User.objects.count(),
            "users_with_tokens": users_with_tokens.count(),
            "users_without_tokens": User.objects.filter(reg_token__isnull=True).count()
        },
        "token_details": [
            {
                "name": token.name,
                "token_code": token.token_code,
                "is_active": token.is_active,
                "usage": f"{token.current_usage}/{token.max_usage if token.max_usage > 0 else 'unlimited'}",
                "registered_users": token.registered_users.count(),
                "expires_at": token.expires_at
            }
            for token in tokens
        ]
    }
    
    return Response(stats)
