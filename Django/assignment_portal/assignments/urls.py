from django.urls import path
from .views import *
from .api_views import assignment_list

urlpatterns = [
    path('teacher-dashboard/',teacher_dashboard,name='teacher_dashboard'),
    path('create-assignment/',create_assignment,name='create_assignment'),
    path('delete-assignment/<int:assignment_id>/',delete_assignment,name='delete_assignment'),
    path('api/assignments/',assignment_list,name='assignment_list_api'),

]
