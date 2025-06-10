from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    ProfileView,
    validate_registration_token,
    registration_info,
    token_statistics
)

urlpatterns = [
    # Registration with token validation
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('validate-token/', validate_registration_token, name='validate_registration_token'),
    path('registration-info/', registration_info, name='registration_info'),
    
    # Authentication
    path('login/', LoginView.as_view(), name='auth_login'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    
    # Token management
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Password management
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    
    # User profile
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # Admin endpoints
    path('token-stats/', token_statistics, name='token_statistics'),
]
