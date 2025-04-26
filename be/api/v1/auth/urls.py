from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    ProfileView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', TokenObtainPairView.as_view(), name='auth_login'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('profile/', ProfileView.as_view(), name='profile'),
]