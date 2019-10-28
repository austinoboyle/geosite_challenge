from rest_framework.response import Response


def require_login_or_401(function):
    """Decorates a view to require authentication.

    Args:
        function: view function

    Returns:
        Decorated function
    """
    def wrap(request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response({"detail": "Must be logged in."}, status=401)
        return function(request, *args, **kwargs)
    return wrap
