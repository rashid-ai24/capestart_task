import uuid
from django.db import models
from django.conf import settings


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    department = models.CharField(max_length=100)
    credits = models.PositiveIntegerField(default=3)
    semester = models.PositiveIntegerField()
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='courses_teaching')
    max_enrollment = models.PositiveIntegerField(default=60)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['course_code']

    def __str__(self):
        return f"{self.course_code} - {self.name}"


class CourseSection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    section_number = models.CharField(max_length=10)
    schedule = models.JSONField(default=dict)
    room = models.CharField(max_length=50, blank=True)
    capacity = models.PositiveIntegerField(default=30)
    enrolled_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['course', 'section_number']

    def __str__(self):
        return f"{self.course.course_code} - Section {self.section_number}"


class Enrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='enrollments')
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('enrolled', 'Enrolled'),
        ('dropped', 'Dropped'),
        ('waitlisted', 'Waitlisted'),
        ('completed', 'Completed'),
    ], default='enrolled')
    grade = models.CharField(max_length=2, blank=True)

    class Meta:
        unique_together = ['student', 'section']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.student.student_id} - {self.section}"
