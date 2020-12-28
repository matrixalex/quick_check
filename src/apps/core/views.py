from django.db.models import Q
from django.shortcuts import redirect, render

from src.apps.core.models import StudyClass
from src.apps.core.service import parse_date
from src.apps.homework.models import Homework
from src.apps.users.models import RegistrationRequest, User
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
        return redirect('/auth/')
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
    return render(request, 'admin.html', context=data)


def teacher_page(request):
    user = request.user
    data = {'user': user, 'org': user.org}
    if user.status.id != TEACHER:
        return redirect('/not-allowed')
    study_class_id = request.GET.get('study_class_id')
    pupils_id = request.GET.get('pupils_id')
    if pupils_id:
        pupils_id = [
            int(pupil_id.strip())
            for pupil_id in
            str(pupils_id).replace('[', '').replace(']', '').split(',')
        ]
    study_classes = StudyClass.objects.filter(teachers__in=[user])
    data['study_classes'] = study_classes
    pupils = User.objects.filter(org=user.org, status=PUPIL, study_class__in=study_classes)
    print(pupils)
    homeworks = Homework.objects.filter(homework_teacher=user)
    if study_class_id:
        pupils = pupils.filter(study_class_id=study_class_id)
    if pupils_id:
        pupils = pupils.filter(id__in=pupils_id)
    date_filter = Q()
    if request.GET.get('created_at_gte'):
        date_filter &= Q(created_at__gte=parse_date(request.GET.get('created_at__gte')))
    if request.GET.get('created_at_lte'):
        date_filter &= Q(created_at__lte=parse_date(request.GET.get('created_at_lte')))
    homeworks = homeworks.filter(pupil_homework_exercise__pupil__in=pupils).filter(date_filter).distinct()

    data['pupils'] = pupils
    data['homeworks'] = homeworks
    return render(request, 'teacher.html', context=data)


def pupil_page(request):
    user = request.user
    data = {'user': user}
    if user.status.id != PUPIL:
        return redirect('/not-allowed')
    return render(request, 'pupil.html', context=data)
