from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .models import Profile


def role_required(role):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            profile = Profile.objects.get(user=request.user)
            if profile.role != role:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


doctor_required = role_required('DOCTOR')
patient_required = role_required('PATIENT')
