from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView,DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import role_required
from django.http import HttpResponseForbidden
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