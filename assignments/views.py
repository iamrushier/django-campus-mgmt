from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.utils import timezone

from accounts.decorators import role_required
from .models import Assignment, Submission
from courses.models import Course
from .forms import AssignmentForm, SubmissionForm

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


@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)

    if request.user.role == "student":
        enrolled = request.user.enrollments.filter(course=assignment.course).exists()
        if not enrolled:
            return HttpResponseForbidden("You are not enrolled in this course.")
    else:
        enrolled = True  # teachers/admins

    if request.user.role == "teacher":
        if assignment.course.teacher != request.user:
            return HttpResponseForbidden("You are not the teacher of this course.")

    return render(
        request,
        "assignments/assignment_detail.html",
        {"assignment": assignment, "enrolled": enrolled},
    )

    
@login_required
@role_required(["teacher", "admin"])
def assignment_edit(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    
    if request.user.role == "teacher" and assignment.course.teacher != request.user:
        return HttpResponseForbidden("You cannot edit this assignment.")
    
    if request.method == "POST":
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.course = assignment.course  # prevent course change
            updated.teacher = assignment.teacher  # preserve original teacher
            updated.save()
            messages.success(request, "Assignment updated successfully.")
            return redirect("assignments:assignment_detail", pk=assignment.pk)
    else:
        form = AssignmentForm(instance=assignment)
    return render(
        request,
        "assignments/assignment_form.html",
        {"form": form, "assignment": assignment, "is_edit": True},
    )
    
    
@login_required
@role_required(["teacher", "admin"])
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.user.role == "teacher" and assignment.course.teacher != request.user:
        return HttpResponseForbidden("You cannot delete this assignment.")
    if request.method == "POST":
        course_pk = assignment.course.pk
        assignment.delete()
        messages.success(request, "Assignment deleted successfully.")
        return redirect("assignments:course_assignments", course_pk=course_pk)
    return render(
        request,
        "assignments/assignment_confirm_delete.html",
        {"assignment": assignment},
    )


############## Submission Related Views ################

@login_required
@role_required(["teacher", "admin"])
def assignment_submissions(request, assignment_pk):
    assignment = get_object_or_404(Assignment, pk=assignment_pk)
    if request.user.role == "teacher" and assignment.course.teacher != request.user:
        return HttpResponseForbidden("You cannot view submissions for this assignment.")
    
    submissions = assignment.submissions.select_related("student")
    return render(
        request,
        "submissions/submission_list.html",
        {"assignment": assignment, "submissions": submissions},
    )
    
@login_required
@role_required(['student'])
def submit_assignment(request, assignment_pk):
    assignment = get_object_or_404(Assignment, pk=assignment_pk)

    if not request.user.enrollments.filter(course=assignment.course).exists():
        return HttpResponseForbidden("You are not enrolled in this course.")

    try:
        submission = Submission.objects.get(assignment=assignment, student=request.user)
        already_submitted = True
    except Submission.DoesNotExist:
        submission = None
        already_submitted = False
        
    if assignment.due_date and timezone.now() > assignment.due_date:
        messages.error(request, "Deadline has passed.")
        return redirect('assignments:assignment_detail', pk=assignment.pk)
    
    if request.method == 'POST' and not already_submitted:
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            Submission.objects.create(
                assignment=assignment,
                student=request.user,
                file=form.cleaned_data['file']
            )
            messages.success(request, "Assignment submitted successfully.")
            return redirect('assignments:assignment_detail', pk=assignment.pk)
    else:
        form = SubmissionForm() if not already_submitted else None

    return render(request, "submissions/submission_form.html", {
        "assignment": assignment,
        "form": form,
        "submission": submission,
        "already_submitted": already_submitted
    })
