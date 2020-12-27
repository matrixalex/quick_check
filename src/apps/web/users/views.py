from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from src.apps.core.service import get_all_orgs, get_org_by_id, get_study_class_by_id, get_study_classes
from src.apps.core.api import BaseCreateOrChangeView, BaseDeleteView
from src.apps.users import service
from src.apps.users.models import User, RegistrationRequest, UserLog
from src.apps.users.models.registration_request import RegistrationStatus
from src.apps.users.models import user_type
from django.views import View


REDIRECT_URLS = {
    user_type.SYSTEM_ADMIN: 'system-admins',
    user_type.ADMIN: 'admins',
    user_type.TEACHER: 'teachers',
    user_type.PUPIL: 'pupils'
}


class UserListView(View):
    TEMPLATE_NAME = ''
    USER_TYPE_FILTER_ID = user_type.SYSTEM_ADMIN

    def get_data(self, request):
        data = {
            'user': request.user,
            'user_type_id': self.USER_TYPE_FILTER_ID,
            'user_types': user_type,
            'users': User.objects.not_superusers().filter(status__id=self.USER_TYPE_FILTER_ID)
        }
        if request.user.org:
            data['users'] = data['users'].filter(org=request.user.org)
        data['verifications'] = [user[0] for user in data['users'].filter(
            user_registration_request__isnull=False,
            user_registration_request__is_deleted=False,
        ).values_list('id')]
        data['users_count'] = data['users'].count()
        data['verifications_count'] = len(data['verifications'])
        return data

    def get(self, request):
        data = self.get_data(request)
        extra_data = get_extra_context_by_user_type(request, self.USER_TYPE_FILTER_ID)
        data.update(extra_data)
        return render(request, 'users_wrapper.html', context=data)


class UsersView(UserListView):
    def get(self, request):
        self.USER_TYPE_FILTER_ID = request.GET.get('user_type', user_type.PUPIL)
        return super(UsersView, self).get(request)


class UserCreateOrChangeView(BaseCreateOrChangeView):
    model = User
    _fields = {
        'id': {
            'type': BaseCreateOrChangeView.FieldTypeEnumerate.STR,
            'validator': lambda val: int(val) > 0
        },
        'first_name': {
            'type': BaseCreateOrChangeView.FieldTypeEnumerate.STR,
            'required': True
        },
        'last_name': {
            'type': BaseCreateOrChangeView.FieldTypeEnumerate.STR,
            'required': True
        },
        'middle_name': {
            'type': BaseCreateOrChangeView.FieldTypeEnumerate.STR,
            'required': True
        },
        'phone_number': {
            'type': BaseCreateOrChangeView.FieldTypeEnumerate.STR,
            'required': True
        },
        'email': {
            'type': BaseCreateOrChangeView.FieldTypeEnumerate.STR,
            'required': True
        },
        'birth_date': {
            'type': BaseCreateOrChangeView.FieldTypeEnumerate.DATE,
            'required': True
        },
        'status': {
            'type': BaseCreateOrChangeView.FieldTypeEnumerate.FOREIGN_KEY,
            'required': True,
            'model': user_type.UserType
        }
    }

    def extra_post(self, request):
        org_id = request.data.get('org_id')
        if org_id:
            org = get_org_by_id(org_id)
            service.set_org(self.obj, org)
        study_class_id = request.data.get('study_class_id')
        if study_class_id:
            study_class = get_study_class_by_id(study_class_id)
            service.set_study_class(self.obj, study_class)
        password = request.data.get('password')
        password_confirm = request.data.get('password_confirm')
        if password and password_confirm and password == password_confirm:
            service.change_user_password(self.obj, password)
            UserLog.objects.create(log_user=self.obj, text='Пользователю {}:{} задан пароль {}'.format(
                self.obj.id, self.obj, password
            ))
        elif not (password and password_confirm) and not request.data.get('id'):
            # Создание юзера, генерим пароль если не передали]
            password = service.generate_random_password()
            service.change_user_password(self.obj, password)
            UserLog.objects.create(log_user=self.obj, text='Пользователю {}:{} задан пароль {}'.format(
                self.obj.id, self.obj, password
            ))
        if not self.obj.is_accepted:
            self.obj.is_accepted = True
            self.obj.save()


class BlockUserView(APIView):
    @staticmethod
    def post(request, user_id):
        user = request.user
        user_to_block = service.get_user_by_id(user_id)
        status = bool(int(request.data.get('status', 1)))
        user_to_block.is_accepted = status
        user_to_block.save()
        return Response({'result': {'status': True}}, HTTP_200_OK)


class AcceptRegistrationView(APIView):
    @staticmethod
    def get(request, user_id):
        registration_request = RegistrationRequest.objects.get(registration_user_id=user_id)
        return Response({'result': {'text': registration_request.registration_reason}}, HTTP_200_OK)

    @staticmethod
    def post(request, user_id):
        registration_request = RegistrationRequest.objects.get(registration_user_id=user_id)
        status = bool(int(request.data.get('status', 1)))
        registration_request.status = RegistrationStatus.ACCEPTED if status else RegistrationStatus.NOT_ACCEPTED
        registration_request.save()
        return Response({'result': {'status': True}}, HTTP_200_OK)


def get_extra_context_by_user_type(request, user_type_id):
    """Получить дополнительный словарь контекста по типу учетной записи"""
    if isinstance(user_type_id, str):
        user_type_id = int(user_type_id)
    if user_type_id == user_type.ADMIN:
        return {'orgs': get_all_orgs()}
    elif user_type_id == user_type.TEACHER:
        return {'org': request.user.org}
    elif user_type_id == user_type.PUPIL:
        print('pupil')
        return {'study_classes': get_study_classes(request.user.org), 'org': request.user.org}
    return {}


class UserDeleteView(BaseDeleteView):
    model = User
