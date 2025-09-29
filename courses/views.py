from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView,DetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from accounts.decorators import role_required
from django.http import HttpResponseForbidden
from django.core import mail

from accounts.models import CMSUser
from courses.forms import CourseForm, GradeUpdateForm
from .models import Course, Enrollment

class CourseListView(ListView):
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"

class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = context['course']
        context['enrollment'] = None
        user = self.request.user
        if user.is_authenticated and user.role == 'student':
            try:
                enrollment = Enrollment.objects.get(student=user, course=course)
                context['enrollment'] = enrollment
            except Enrollment.DoesNotExist:
                pass
                
        return context
    
@login_required
@role_required(['student',])
def enroll_in_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
    if created:
        messages.success(request,f"You are now enrolled in {course.name}")
        mail.send_mail(
            "Enrollment success",
            f"You have successfully enrolled in course {course.name}\n"+
            f"Here are the enrollment details: {str(enrollment)}",
            'from@example.com',
            [enrollment.student.email,]
        )
    else:
        messages.info(request,f"You are already enrolled in this course")
    return redirect('courses:course_detail',pk=pk)

@login_required
@role_required(['teacher', 'admin'])
def enrolled_students(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user.role == 'teacher' and course.teacher != request.user:
        return HttpResponseForbidden("You are not the teacher of this course.")
    enrollments = course.enrollments.select_related('student')
    return render(request, 'courses/enrolled_students.html', {'course': course, 'enrollments': enrollments})


@login_required
def course_results(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user.role == 'student':
        enrollment = get_object_or_404(Enrollment, course=course, student=request.user)
        return render(request, 'courses/results.html', {'course': course, 'enrollment': enrollment})
    elif request.user.role in ['teacher','admin']:
        if request.user.role=='teacher' and course.teacher!=request.user:
            return HttpResponseForbidden("You are not the teacher of this course")
        enrollments=course.enrollments.select_related('student')
        return render(request, 'courses/results.html',{'course':course,'enrollments':enrollments})
    else:
        return HttpResponseForbidden("Unauthorized")
    

def is_teacher_or_admin(user:CMSUser):
    return user.is_authenticated and user.role in ("teacher", "admin")

@login_required
@user_passes_test(is_teacher_or_admin)
def update_grade(request, course_pk, enrollment_pk):
    enrollment= get_object_or_404(Enrollment, pk=enrollment_pk, course_id=course_pk)
    
    if request.user.role == "teacher":
        if not enrollment.course.teacher or enrollment.course.teacher != request.user:
            return HttpResponseForbidden("You are not the teacher of this course")
    if request.method == "POST":
        form = GradeUpdateForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            mail.send_mail(
            "Grading updates",
            f"Your progress has been graded for course {enrollment.course.name}\n"+
            f"You got grade: {str(enrollment.grade)}\nKeep it up!",
            'from@example.com',
            [enrollment.student.email,]
        )
            return redirect("courses:results", pk=course_pk)
    else:
        form = GradeUpdateForm(instance=enrollment)
        
    return render(request, "courses/update_grade.html", {"form": form, "enrollment": enrollment})
    

@login_required
@role_required(["teacher", "admin"])
def course_create(request):
    if request.method=='POST':
        form= CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            if request.user.role == 'teacher':
                course.teacher = request.user
            course.save()
            messages.success(request,f"Course {course.code} created successfully")
            return redirect("courses:course_detail",pk=course.pk)
    else:
        form=CourseForm()
    return render(request, 'courses/course_form.html',{'form':form,'title':"Create Course"})

@login_required
@role_required(["teacher", "admin"])
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.user.role == "teacher" and course.teacher != request.user:
        return HttpResponseForbidden("You are not the teacher of this course.")

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f"Course {course.code} updated successfully.")
            return redirect("courses:course_detail", pk=course.pk)
    else:
        form = CourseForm(instance=course)

    return render(request, "courses/course_form.html", {"form": form, "title": f"Edit {course.code}"})


@login_required
@role_required(["teacher", "admin"])
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    
    if request.user.role == "teacher" and course.teacher != request.user:
        return HttpResponseForbidden("You are not the teacher of this course.")

    if request.method == "POST":
        course.delete()
        messages.success(request, f"Course {course.code} deleted successfully.")
        return redirect("courses:course_list")

    return render(request, "courses/course_confirm_delete.html", {"course": course})
