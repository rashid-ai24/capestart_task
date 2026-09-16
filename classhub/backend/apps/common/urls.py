"""
ClassHub Common URLs
"""
from django.urls import path
from . import views

app_name = 'common'

urlpatterns = [
    # Health check endpoints
    path('health/', views.HealthCheckView.as_view(), name='health-check'),
    path('ready/', views.ReadinessCheckView.as_view(), name='readiness-check'),
    path('alive/', views.LivenessCheckView.as_view(), name='liveness-check'),
    path('version/', views.VersionView.as_view(), name='version'),
]
