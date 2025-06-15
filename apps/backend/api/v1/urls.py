from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.v1.auth.urls')),
    # path('dashboard/', include('api.v1.dashboard.urls')),
    path('finance/', include('api.v1.finance.urls')),
    path('invest/', include('api.v1.invest.urls')),
]