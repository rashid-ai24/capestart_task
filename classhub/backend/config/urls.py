"""
ClassHub URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # ============================================
    # Django Admin
    # ============================================
    path('admin/', admin.site.urls),
    
    # ============================================
    # API v1 Routes
    # ============================================
    path('api/v1/', include('apps.authentication.urls')),
    path('api/v1/', include('apps.students.urls')),
    path('api/v1/', include('apps.courses.urls')),
    path('api/v1/', include('apps.attendance.urls')),
    path('api/v1/', include('apps.grades.urls')),
    path('api/v1/', include('apps.assignments.urls')),
    path('api/v1/', include('apps.fees.urls')),
    path('api/v1/', include('apps.communications.urls')),
    path('api/v1/', include('apps.reports.urls')),
    
    # ============================================
    # API Schema (drf-spectacular)
    # ============================================
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # ============================================
    # Health Check
    # ============================================
    path('health/', include('apps.common.urls')),
]

# ============================================
# Media Files (Development)
# ============================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# ============================================
# Admin Site Customization
# ============================================
admin.site.site_header = 'ClassHub Administration'
admin.site.site_title = 'ClassHub Admin'
admin.site.index_title = 'Welcome to ClassHub Administration'
