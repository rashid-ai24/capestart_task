from django.urls import path
from .views import *
from .api_views import submission_list

urlpatterns = [
    path('student/dashboard/',student_dashboard,name='student_dashboard'),
    path('submit/<int:assignment_id>/',submitted_assignment,name='submit_assignment'),
    path('view-submissions/<int:assignment_id>/',view_submissions,name='view_submissions'),
    path('api/submissions/',submission_list,name='submission_list_api'),
]
