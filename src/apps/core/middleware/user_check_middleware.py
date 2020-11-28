from django.shortcuts import redirect
REDIRECT_EXCLUDE_PATHS = ['/auth/logout', '/not-allowed']


class UserCheckMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.path not in REDIRECT_EXCLUDE_PATHS:
            user_can_use_site = request.user.check_site_permission()
            if not user_can_use_site:
                return redirect('/not-allowed')
        response = self._get_response(request)
        return response
