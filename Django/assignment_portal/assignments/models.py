from django.db import models
from django.contrib.auth.models import User


class Assignment(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title