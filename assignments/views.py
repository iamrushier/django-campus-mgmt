from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

from accounts.decorators import role_required

from .models import Assignment
from courses.models import Course
from .forms import AssignmentForm

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

@login_required
@role_required(["teacher","admin"])
def assignment_create(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if request.user.role == "teacher" and course.teacher != request.user:
        return HttpResponseForbidden("You are not allowed to add assignments to this course.")
    
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.teacher = course.teacher or request.user  # ensure teacher is set
            assignment.save()
            messages.success(request, "Assignment created successfully.")
            return redirect("assignments:course_assignments", course_pk=course.pk)
    else:
        form = AssignmentForm()
    return render(request, "assignments/assignment_form.html", {"form": form, "course": course})