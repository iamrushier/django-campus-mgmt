from django.urls import path
from .views import course_assignments,assignment_create,assignment_detail,assignment_edit,assignment_delete
from .views import assignment_submissions
app_name = "assignments"

urlpatterns = [
    path("course/<int:course_pk>/", course_assignments, name="course_assignments"),
    path("course/<int:course_pk>/create/", assignment_create, name="assignment_create"),
    path("<int:pk>/", assignment_detail, name="assignment_detail"),
    path("<int:pk>/edit/", assignment_edit, name="assignment_edit"),
    path("<int:pk>/delete/", assignment_delete, name="assignment_delete"),
    
    path("<int:assignment_pk>/submissions/", assignment_submissions, name="assignment_submissions"),
]