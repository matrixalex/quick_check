from django.shortcuts import redirect
from src.apps.users.models import user_type
REDIRECT_EXCLUDE_PATHS = ['/auth/logout', '/not-allowed', '/auth/login', '/pupil/templates', '/pupil/upload-template']


class TemplateUploadCheckMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request, *args, **kwargs):
        if (request.user.is_authenticated and request.path not in REDIRECT_EXCLUDE_PATHS and
                request.user.status.id == user_type.PUPIL):
            user_can_use_site = request.user.is_any_template_uploaded
            if not user_can_use_site:
                return redirect('/pupil/templates')
        response = self._get_response(request)
        return response
