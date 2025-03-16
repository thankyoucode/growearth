# decorators.py
from functools import wraps

from django.http import Http404


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404(
                "This page does not exist."
            )  # Raise a 404 error instead of forbidden
        return view_func(request, *args, **kwargs)

    return _wrapped_view
