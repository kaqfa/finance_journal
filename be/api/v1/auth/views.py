# from django.contrib.auth.models import User
from master.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    LoginSerializer,
    PasswordChangeSerializer,
    PasswordResetSerializer,
    RegTokenValidationSerializer
)


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    """
    Enhanced User Registration dengan Registration Token validation
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer
    
    @swagger_auto_schema(
        operation_summary="User Registration",
        operation_description="Register user baru dengan registration token",
        responses={
            201: openapi.Response(
                description="Registrasi berhasil",
                examples={
                    "application/json": {
                        "message": "Registrasi berhasil! Selamat datang di Journal Invest.",
                        "user": {"id": 1, "username": "newuser", "email": "new@example.com"},
                        "tokens": {
                            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Data tidak valid atau token tidak valid",
                examples={
                    "application/json": {
                        "token_registrasi": ["Token registrasi tidak valid."]
                    }
                }
            )
        }
    )
    
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


@swagger_auto_schema(
    method='post',
    request_body=RegTokenValidationSerializer,
    responses={
        200: openapi.Response(
            description="Token valid",
            examples={
                "application/json": {
                    "token_name": "Alpha Testing Token",
                    "token_code": "ALPHA2025",
                    "remaining_usage": "Unlimited",
                    "expires_at": "2025-12-31T23:59:59Z",
                    "is_valid": True,
                    "message": "Token valid dan dapat digunakan untuk registrasi"
                }
            }
        ),
        400: openapi.Response(
            description="Token tidak valid",
            examples={
                "application/json": {
                    "error": "Token tidak valid",
                    "details": {"token_code": ["Token registrasi tidak ditemukan."]}
                }
            }
        )
    },
    operation_description="Validasi registration token sebelum registrasi",
    operation_summary="Validate Registration Token"
)
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


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """
    Enhanced Login dengan informasi registration token
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Login berhasil",
                examples={
                    "application/json": {
                        "message": "Selamat datang kembali, John Doe!",
                        "tokens": {
                            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                        },
                        "user": {
                            "id": 1,
                            "username": "johndoe",
                            "email": "john@example.com"
                        }
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized - Username atau password salah",
                examples={
                    "application/json": {
                        "error": "Username atau password salah"
                    }
                }
            )
        },
        operation_description="Login untuk mendapatkan JWT access dan refresh token",
        operation_summary="User Login"
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {"error": "Data tidak valid", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        
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


@method_decorator(csrf_exempt, name='dispatch')
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


@method_decorator(csrf_exempt, name='dispatch')
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


@method_decorator(csrf_exempt, name='dispatch')
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


@method_decorator(csrf_exempt, name='dispatch')
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
