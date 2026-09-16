from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    role = (
        ('teacher','Teacher'),
        ('student','Student')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=8, choices=role)
    
    def __str__(self):
        return self.user.username