from django.core.exceptions import PermissionDenied
from django.http import Http404
def user_type_required(allowed_type=[]):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if request.user.user_type in allowed_type:
                return view_func(request, *args, **kwargs)
            else:
                raise Http404
        return wrap
    return decorator