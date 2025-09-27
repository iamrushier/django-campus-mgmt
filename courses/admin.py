from django.contrib import admin
from .models import Course, Enrollment

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    readonly_fields = ('enrolled_on',)
    
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code','name','teacher')
    search_fields = ('code','name','teacher__username','teacher__email')
    inlines = [EnrollmentInline]
    
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('course','student','enrolled_on','grade')
    list_filter = ('course',)
    search_fields = ('student__username','student__email','course__code','course__name')
    

admin.site.register(Course,CourseAdmin)
admin.site.register(Enrollment,EnrollmentAdmin)
