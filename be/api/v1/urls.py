from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.v1.auth.urls')),
    # path('journal/', include('api.v1.journal.urls')),
    # path('dashboard/', include('api.v1.dashboard.urls')),
    # Finance akan diimplementasikan nanti
    # path('finance/', include('api.v1.finance.urls')),
]