# courses/forms.py
from django import forms
from .models import Enrollment, Course

class GradeUpdateForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ["grade"]
        
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "code", "description"]