from django.urls import path
from .views import course_assignments,assignment_create

app_name = "assignments"

urlpatterns = [
    path("course/<int:course_pk>/", course_assignments, name="course_assignments"),
    path("course/<int:course_pk>/create/", assignment_create, name="assignment_create"),
]