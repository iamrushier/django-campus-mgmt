from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CMSUser(AbstractUser):
    ROLE_CHOICES = [
        ('student','Student'),
        ('teacher','Teacher'),
        ('admin','Admin')
    ]
    email=models.EmailField(unique=True)
    role=models.CharField(max_length=20,choices=ROLE_CHOICES,default='student')
    
    def __str__(self):
        return f"{self.username} {self.role}"
    