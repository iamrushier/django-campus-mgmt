from django.db import models
from django.conf import settings

class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20,unique=True)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role':'teacher'},
        related_name='courses_taught'
    )
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    

class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments', # student.enrollments to get all for student
        limit_choices_to={'role':'student'}
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        related_name='enrollments' # course.enrollments to get for the course
    )
    enrolled_on = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=10, blank=True,null=True)
    
    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-enrolled_on']
        
    def __str__(self):
        return f"{self.student.username} in {self.course.code}"