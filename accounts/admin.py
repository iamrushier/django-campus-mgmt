from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CMSUser

class CMSUserAdmin(UserAdmin):
    model=CMSUser
    fieldsets=UserAdmin.fieldsets + (
        ('Additional Info',{'fields':('role',)}),
    )
    # throwing away Django’s default add_fieldsets - None
    add_fieldsets=(
        (None,{
            'classes':('wide',),
            'fields':('username','email','role','password1','password2'),
        }),
    )
    list_display = ['id','username','email','role','is_staff']
    
admin.site.register(CMSUser,CMSUserAdmin)