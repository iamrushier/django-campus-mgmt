# courses/urls.py
from django.urls import path
from .views import (
    CourseListView, CourseDetailView,
    enroll_in_course, enrolled_students, course_results, update_grade,
    course_create,course_update,course_delete
)

app_name = 'courses'

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('<int:pk>/enroll/', enroll_in_course, name='enroll'),
    path('<int:pk>/students/', enrolled_students, name='enrolled_students'),
    path('<int:pk>/results/', course_results, name='results'),
    path("<int:course_pk>/students/<int:enrollment_pk>/grade/", update_grade, name="update_grade"),
    
    path('course_create/',course_create,name="course_create"),
    path('<int:pk>/edit/',course_update,name="course_update"),
    path("<int:pk>/delete/", course_delete, name="course_delete"),
]
