import uuid
from django.db import models


class Grade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='grades')
    assignment = models.ForeignKey('assignments.Assignment', on_delete=models.CASCADE, related_name='grades', null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    grade_letter = models.CharField(max_length=2, blank=True)
    comments = models.TextField(blank=True)
    graded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-graded_at']

    def __str__(self):
        return f"{self.student.student_id} - {self.course.course_code} - {self.score}"

    @property
    def percentage(self):
        if self.max_score > 0:
            return (self.score / self.max_score) * 100
        return 0
