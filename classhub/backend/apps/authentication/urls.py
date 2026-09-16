"""
ClassHub Authentication URLs
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = 'authentication'

urlpatterns = [
    # ============================================
    # Authentication Endpoints
    # ============================================
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # ============================================
    # Profile Endpoints
    # ============================================
    path('auth/profile/', views.ProfileView.as_view(), name='profile'),
    path('auth/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    
    # ============================================
    # Password Reset Endpoints
    # ============================================
    path('auth/password-reset/', views.PasswordResetRequestView.as_view(), name='password-reset'),
    path('auth/password-reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    
    # ============================================
    # MFA Endpoints
    # ============================================
    path('auth/mfa/enable/', views.MFAEnableView.as_view(), name='mfa-enable'),
    path('auth/mfa/disable/', views.MFADisableView.as_view(), name='mfa-disable'),
    path('auth/mfa/verify/', views.VerifyMFAView.as_view(), name='mfa-verify'),
    
    # ============================================
    # User Management Endpoints (Admin)
    # ============================================
    path('auth/users/', views.UserListView.as_view(), name='user-list'),
    path('auth/users/<uuid:pk>/', views.UserDetailView.as_view(), name='user-detail'),
]
