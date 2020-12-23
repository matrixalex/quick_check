class CsrfDisable:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request, *args, **kwargs):
        setattr(request, '_dont_enforce_csrf_checks', True)
        response = self._get_response(request)
        return response
