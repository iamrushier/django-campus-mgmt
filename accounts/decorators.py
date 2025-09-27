from functools import wraps
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden,HttpRequest
from accounts.models import CMSUser

def role_required(allowed_roles):
    # use as decorator @role_required(['student']) or @role_required(['teacher','admin'])
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request:HttpRequest, *args, **kwargs):
            user:CMSUser = request.user  # type indication for auto suggestion
            if not user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if user.role in allowed_roles:
                return view_func(request,*args,**kwargs)    
            return HttpResponseForbidden("You are not authorized to view this page.")
        return _wrapped_view
    return decorator
        