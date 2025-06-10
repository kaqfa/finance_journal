"""
URL configuration for wealthwise project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Schema view for Swagger/OpenAPI documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Journal Invest API",
        default_version='v1',
        description="""
        Dokumentasi API untuk aplikasi Journal Invest - Finance & Investment Tracker
        
        ## Authentication
        API ini menggunakan JWT (JSON Web Token) untuk authentication.
        
        ### Cara menggunakan:
        1. Login via `/api/v1/auth/login/` untuk mendapatkan access token
        2. Klik tombol "Authorize" di kanan atas
        3. Masukkan token dengan format: `Bearer your_access_token_here`
        4. Klik "Authorize" untuk menyimpan token
        5. Sekarang Anda bisa mengakses endpoint yang membutuhkan authentication
        
        ### Format Authorization Header:
        ```
        Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
        ```
        """,
        contact=openapi.Contact(email="fahri@sembarang.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('master.urls', namespace='application')),

    # Swagger Documentation URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/v1/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-alt'),  # Shortcut URL
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-docs'),  # Alternative URL
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

# urlpatterns += i18n_patterns(
#     path('dashboard/', include('dashboard.urls', namespace='dashboard')),
# )