from django.contrib import admin
from .models import Assignment, Submission

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display=("title", "course", "due_date", "created_at", "updated_at")
    list_filter=("course", "due_date", "created_at")
    search_fields=("title", "description", "course__code", "course__name")
    autocomplete_fields=("course",)
    

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("assignment", "student", "submitted_at", "grade")
    list_filter = ("assignment__course", "grade", "submitted_at")
    search_fields = ("student__username", "assignment__title")
    autocomplete_fields = ("assignment", "student")