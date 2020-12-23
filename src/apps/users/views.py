from django.contrib.auth import logout
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from rest_framework.views import APIView

from . import service as user_services
from .models.user_type import UserType, PUPIL
from ..core.errors import ErrorMessages
from src.quick_check import settings
from ..core.message import DataInfoMessage
from ..core.service import parse_date
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.response import Response


class AuthView(View):
    """Лендинг и авторизация\регистрация"""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        context = {'user_types': UserType.choices}
        return render(request, 'index.html', context=context)


class LoginView(APIView):
    """Аторизация пользователя"""

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        data = user_services.authenticate(request, email, password)
        if not data.status:
            return Response({'result': {'message': data.message}}, HTTP_400_BAD_REQUEST)
        data = {'result': user_services.serialize_user(data.user, short=True)}
        return Response(data, HTTP_200_OK)


class RegistrationView(APIView):
    """Регистрация пользователя"""

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        middle_name = request.POST.get('middle_name', '')
        phone_number = request.POST.get('phone_number')
        registration_reason = request.POST.get('registration_reason', '')
        birth_date = parse_date(request.POST.get('birth_date'))
        user_type = int(request.POST.get('user_type', PUPIL))
        status, message = user_services.register_user(first_name, last_name, email, phone_number, password, birth_date,
                                                      middle_name=middle_name, registration_reason=registration_reason,
                                                      user_profile_type=user_type)
        if not status:
            return Response({'result': {'message': message}}, HTTP_400_BAD_REQUEST)
        user_type = UserType.objects.get(pk=user_type)
        data = {'result': {
                'message': DataInfoMessage.REGISTRATION_SUCCESS.format(
                    user_type, user_type.get_superior_user_type())
                }}
        return Response(data, HTTP_200_OK)


class LogoutView(View):
    """Логаут пользователя из системы"""

    def get(self, request):
        logout(request)
        return redirect('/')


class ResetPasswordPageView(View):
    """Страница восстановления пароля"""

    def get(self, request):
        error = None
        if not settings.PASSWORD_RESET_ACTIVE:
            error = ErrorMessages.PASSWORD_RESET_NOT_ACTIVE
        return render(request, 'reset_password.html', context={'error': error})

    def post(self, request):
        if not settings.PASSWORD_RESET_ACTIVE:
            return redirect('/')
        email = request.POST.get('email')
        user = user_services.get_user_by_email(email)
        if not user:
            return render(request, 'reset_password.html', context={'error': ErrorMessages.NO_USER})
        user_services.start_reset_password_session(user)
        return render(request, 'reset_password.html')


class ResetPassword(View):
    """Восстановление пароля"""

    def get(self, request, uuid):
        error = None
        if not settings.PASSWORD_RESET_ACTIVE:
            error = ErrorMessages.PASSWORD_RESET_NOT_ACTIVE
        user = user_services.get_user_by_uuid(uuid)
        if not user:
            error = ErrorMessages.NO_USER
        return render(request, 'reset_password_confirm.html', context={'user': user, 'error': error})

    def post(self, request, uuid):
        if not settings.PASSWORD_RESET_ACTIVE:
            return redirect('/')
        error = None
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if password != password_confirm:
            error = ErrorMessages.WRONG_PASSWORD
        else:
            user = user_services.get_user_by_uuid(uuid)
            if user:
                user_services.change_user_password(user, password)
        return render(request, 'reset_password_confirm.html', context={'error': error})
