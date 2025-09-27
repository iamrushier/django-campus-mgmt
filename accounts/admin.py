from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CMSUser

class CMSUserAdmin(UserAdmin):
    model=CMSUser
    fieldsets=UserAdmin.fieldsets + (
        ('Additional Info',{'fields':('role',)}),
    )
    add_fieldsets=UserAdmin.add_fieldsets+(
        ('Additional Info',{'fields':('role',)}),
    )
    list_display = ['username','email','role','is_staff']
    
admin.site.register(CMSUser,CMSUserAdmin)