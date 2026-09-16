"""
ClassHub Common Views
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.core.cache import cache
import redis
import os


class HealthCheckView(APIView):
    """Health check endpoint for monitoring."""
    
    permission_classes = []  # No authentication required
    
    def get(self, request, *args, **kwargs):
        health_status = {
            'status': 'healthy',
            'timestamp': self.get_timestamp(),
            'services': {}
        }
        
        # Check database
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            health_status['services']['database'] = {
                'status': 'healthy',
                'message': 'PostgreSQL connection successful'
            }
        except Exception as e:
            health_status['services']['database'] = {
                'status': 'unhealthy',
                'message': str(e)
            }
            health_status['status'] = 'degraded'
        
        # Check Redis cache
        try:
            cache.set('health_check', 'ok', 10)
            cache.get('health_check')
            health_status['services']['cache'] = {
                'status': 'healthy',
                'message': 'Redis connection successful'
            }
        except Exception as e:
            health_status['services']['cache'] = {
                'status': 'unhealthy',
                'message': str(e)
            }
            health_status['status'] = 'degraded'
        
        # Check storage
        try:
            from django.conf import settings
            media_root = settings.MEDIA_ROOT
            if os.path.exists(media_root):
                health_status['services']['storage'] = {
                    'status': 'healthy',
                    'message': 'Media storage accessible'
                }
            else:
                health_status['services']['storage'] = {
                    'status': 'unhealthy',
                    'message': 'Media storage not found'
                }
                health_status['status'] = 'degraded'
        except Exception as e:
            health_status['services']['storage'] = {
                'status': 'unhealthy',
                'message': str(e)
            }
            health_status['status'] = 'degraded'
        
        # Return appropriate status code
        if health_status['status'] == 'healthy':
            return Response(health_status, status=status.HTTP_200_OK)
        else:
            return Response(health_status, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    def get_timestamp(self):
        from django.utils import timezone
        return timezone.now().isoformat()


class ReadinessCheckView(APIView):
    """Readiness check endpoint for Kubernetes."""
    
    permission_classes = []  # No authentication required
    
    def get(self, request, *args, **kwargs):
        """Check if the service is ready to accept traffic."""
        try:
            # Check database connectivity
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            
            return Response({
                'status': 'ready',
                'message': 'Service is ready to accept traffic'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'not_ready',
                'message': str(e)
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class LivenessCheckView(APIView):
    """Liveness check endpoint for Kubernetes."""
    
    permission_classes = []  # No authentication required
    
    def get(self, request, *args, **kwargs):
        """Check if the service is alive."""
        return Response({
            'status': 'alive',
            'message': 'Service is alive'
        }, status=status.HTTP_200_OK)


class VersionView(APIView):
    """Version information endpoint."""
    
    permission_classes = []  # No authentication required
    
    def get(self, request, *args, **kwargs):
        from django.conf import settings
        
        return Response({
            'version': '1.0.0',
            'environment': 'development' if settings.DEBUG else 'production',
            'debug': settings.DEBUG,
        }, status=status.HTTP_200_OK)
