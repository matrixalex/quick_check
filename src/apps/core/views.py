from django.shortcuts import redirect, render


def index(request):
    """
    Корневой url сайта
    :param request: мета данные
    :return: HttpResponse
    """
    user = request.user
    if not user.is_authenticated:
        return redirect('/auth/login')
    if user.is_superuser:
        return redirect('/admin')
    return render(request, 'index.html', context={'user': request.user})


def not_allowed(request):
    """Рендер страницы Нет доступа"""
    return render(request, 'not_allowed.html')
