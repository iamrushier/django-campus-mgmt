from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Assignment
from courses.models import Course

@login_required
def course_assignments(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    
    if request.user.role == "student":
        if not request.user.enrollments.filter(course=course).exists():
            return HttpResponseForbidden("You are not enrolled in this course.")
    elif request.user.role == "teacher":
        if course.teacher != request.user:
            return HttpResponseForbidden("You are not the teacher of this course.")
    # Admin has access to all
    assignments = course.assignments.all() # Reverse relation
    return render(
        request,
        "assignments/assignment_list.html",
        {"course": course, "assignments": assignments},
    )
