# courses/forms.py
from django import forms
from .models import Enrollment

class GradeUpdateForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ["grade"]