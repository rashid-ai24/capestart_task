import uuid
from django.db import models
from django.conf import settings


class AIRecommendation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='ai_recommendations')
    recommendation_type = models.CharField(max_length=20, choices=[
        ('course', 'Course'),
        ('study', 'Study'),
        ('career', 'Career'),
        ('improvement', 'Improvement'),
    ])
    title = models.CharField(max_length=200)
    description = models.TextField()
    confidence_score = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    is_accepted = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.student_id} - {self.title}"


class AIPrediction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='ai_predictions')
    prediction_type = models.CharField(max_length=20, choices=[
        ('performance', 'Performance'),
        ('attendance', 'Attendance'),
        ('dropout', 'Dropout Risk'),
        ('graduation', 'Graduation'),
    ])
    predicted_value = models.JSONField()
    confidence = models.DecimalField(max_digits=3, decimal_places=2)
    factors = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.student_id} - {self.prediction_type}"


class ChatHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_history')
    message = models.TextField()
    response = models.TextField()
    context = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Chat histories'

    def __str__(self):
        return f"{self.user} - {self.created_at}"
