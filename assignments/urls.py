from django.urls import path
from .views import course_assignments

app_name = "assignments"

urlpatterns = [
    path("course/<int:course_pk>/", course_assignments, name="course_assignments"),
]