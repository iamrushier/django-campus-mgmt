# courses/urls.py
from django.urls import path
from .views import (
    CourseListView, CourseDetailView,
    enroll_in_course, enrolled_students, course_results
)

app_name = 'courses'

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('<int:pk>/enroll/', enroll_in_course, name='enroll'),
    path('<int:pk>/students/', enrolled_students, name='enrolled_students'),
    path('<int:pk>/results/', course_results, name='results'),
]
