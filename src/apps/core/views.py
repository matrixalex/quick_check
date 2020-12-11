from django.shortcuts import redirect, render

from src.apps.users.models import RegistrationRequest
from src.apps.users.models.registration_request import RegistrationStatus
from src.apps.users.models.user_type import SYSTEM_ADMIN, ADMIN, TEACHER, PUPIL


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
    if user.status.id == SYSTEM_ADMIN:
        return system_admin_page(request)
    elif user.status.id == ADMIN:
        return admin_page(request)
    elif user.status.id == TEACHER:
        return teacher_page(request)
    else:
        return pupil_page(request)


def not_allowed(request):
    """Рендер страницы Нет доступа"""
    return render(request, 'not_allowed.html')


def system_admin_page(request):
    user = request.user
    data = {'user': user}
    if user.status.id != SYSTEM_ADMIN:
        return redirect('/not-allowed')
    registration_requests = RegistrationRequest.objects.filter(status=RegistrationStatus.WAITING)
    data['system_admins_verification_count'] = registration_requests.filter(
        registration_user__status=SYSTEM_ADMIN
    ).count()
    data['admins_verification_count'] = registration_requests.filter(
        registration_user__status=ADMIN
    ).count()
    return render(request, 'system_admin.html', context=data)


def admin_page(request):
    user = request.user
    data = {'user': user}
    if user.status.id != ADMIN:
        return redirect('/not-allowed')
    if not user.org:
        return redirect('/not-allowed')
    registration_requests = RegistrationRequest.objects.filter(status=RegistrationStatus.WAITING)
    data['teachers_verification_count'] = registration_requests.filter(
        registration_user__status=TEACHER
    ).count()
    data['pupils_verification_count'] = registration_requests.filter(
        registration_user__status=PUPIL
    ).count()
    return render(request, 'index.html', context=data)


def teacher_page(request):
    user = request.user
    data = {'user': user}
    if user.status.id != TEACHER:
        return redirect('/not-allowed')
    return render(request, 'index.html', context=data)


def pupil_page(request):
    user = request.user
    data = {'user': user}
    if user.status.id != PUPIL:
        return redirect('/not-allowed')
    return render(request, 'index.html', context=data)
