from django.shortcuts import render, redirect

from src.apps.core.service import render_error, parse_date, get_all_orgs, get_org_by_id, get_study_class_by_id
from src.apps.core.errors import ErrorMessages
from src.apps.core.api import BaseCreateOrChangeView, BaseDeleteView
from src.apps.users import service
from src.apps.users.models import User, RegistrationRequest
from src.apps.users.models.registration_request import RegistrationStatus
from src.apps.users.models import user_type
from src.apps.users.models.user_type import PUPIL
from django.views import View


REDIRECT_URLS = {
    user_type.SYSTEM_ADMIN: 'system-admins',
    user_type.ADMIN: 'admins',
    user_type.TEACHER: 'teachers',
    user_type.PUPIL: 'pupils'
}


class UserListView(View):
    TEMPLATE_NAME = ''
    USER_TYPE_REQUIRED_ID = None
    USER_TYPE_FILTER_ID = user_type.SYSTEM_ADMIN

    def get_data(self, request):
        data = {'user': request.user,
                'users': User.objects.not_superusers().filter(status__id=self.USER_TYPE_FILTER_ID),
                'verifications': [reg.registration_user.id for reg in RegistrationRequest.objects.filter(
                    status=RegistrationStatus.WAITING,
                    registration_user__status__id=self.USER_TYPE_FILTER_ID)],
                'user_type_id': self.USER_TYPE_FILTER_ID,
                'user_types': user_type
                }
        return data

    def get(self, request):
        if self.USER_TYPE_REQUIRED_ID and request.user.status.id != self.USER_TYPE_REQUIRED_ID:
            return redirect('/not-allowed')
        data = self.get_data(request)
        data.update(get_extra_context_by_user_type(self.USER_TYPE_FILTER_ID))
        return render(request, 'users_wrapper.html', context=data)


class UsersView(UserListView):
    def get(self, request):
        self.USER_TYPE_FILTER_ID = request.GET.get('user_type', user_type.PUPIL)
        self.USER_TYPE_REQUIRED_ID = user_type.SUPERIOR_USER_TYPES.get(self.USER_TYPE_FILTER_ID, user_type.SYSTEM_ADMIN)
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

class UserCreateView(View):
    @staticmethod
    def get(request):
        user_type_id = int(request.GET.get('user_type_id', PUPIL))
        user_type = service.get_user_type(user_type_id)
        data = {'user_type': user_type}
        data.update(get_extra_context_by_user_type(user_type.id))
        if not user_type:
            return render_error(request, ErrorMessages.NO_USER_TYPE)
        return render(request, 'user_create_or_change.html', context=data)

    @staticmethod
    def post(request):
        email = request.POST.get('email')
        password = request.POST.get('password', '')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        middle_name = request.POST.get('middle_name', '')
        phone_number = request.POST.get('phone_number')
        birth_date = parse_date(request.POST.get('birth_date'))
        user_type = int(request.POST.get('user_type', PUPIL))
        status, message = service.register_user(
            first_name,
            last_name,
            email,
            phone_number,
            password,
            birth_date,
            middle_name,
            registration_reason='',
            user_profile_type=user_type,
            create_registration_request=False,
            is_accepted=True
        )
        if not status:
            return render(request, 'user_create_or_change.html', context={
                'user_type': service.get_user_type(user_type),
                'error': message
            })
        return redirect('/users/{}'.format(REDIRECT_URLS[user_type]))


class UserChangeView(View):
    @staticmethod
    def get(request, user_id):
        user_type_id = int(request.GET.get('user_type_id', PUPIL))
        user_to_change = service.get_user_by_id(user_id)
        if not user_to_change:
            return render_error(request, ErrorMessages.NO_USER)
        user_type = service.get_user_type(user_type_id)
        if not user_type:
            return render_error(request, ErrorMessages.NO_USER_TYPE)
        data = {
            'user_type': user_type,
            'user_to_change': user_to_change
        }
        data.update(get_extra_context_by_user_type(user_type_id))
        return render(request, 'user_create_or_change.html', context=data)

    @staticmethod
    def post(request, user_id):
        user = service.get_user_by_id(request.POST.get('user_id'))
        if not user:
            return render_error(request, ErrorMessages.NO_USER)
        email = request.POST.get('email')
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        if password_confirm != password:
            password = ''
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        middle_name = request.POST.get('middle_name', '')
        phone_number = request.POST.get('phone_number')
        birth_date = parse_date(request.POST.get('birth_date'))
        org = get_org_by_id(request.POST.get('org_id', 0))
        user_type = service.get_user_type(int(request.POST.get('user_type', PUPIL)))
        status, message = service.change_user(
            user, first_name, last_name, email, phone_number, user_type, password, birth_date, middle_name, org=org)
        if not status:
            return render(request, 'user_create_or_change.html', context={
                'user_type': user_type,
                'error': message
            })
        return redirect('/users/{}'.format(REDIRECT_URLS[user_type.id]))


class BlockUserView(View):
    @staticmethod
    def get(request, user_id):
        user = request.user
        user_to_block = service.get_user_by_id(user_id)
        if not user_to_block:
            return render_error(request, ErrorMessages.NO_USER)
        status = bool(int(request.GET.get('status', 1)))
        redirect_url = REDIRECT_URLS[int(request.GET.get('user_type_id'))]
        user_to_block.is_accepted = status
        user_to_block.save()
        return redirect('/users/{}'.format(redirect_url))


class AcceptRegistrationView(View):
    @staticmethod
    def get(request, user_id):
        user = service.get_user_by_id(user_id)
        registration_request = RegistrationRequest.objects.get(registration_user=user)
        status = bool(int(request.GET.get('status', 1)))
        registration_request.status = RegistrationStatus.ACCEPTED if status else RegistrationStatus.NOT_ACCEPTED
        registration_request.save()
        return redirect('/users/{}'.format(REDIRECT_URLS[int(request.GET.get('user_type_id'))]))


def get_extra_context_by_user_type(user_type_id):
    """Получить дополнительный словарь контекста по типу учетной записи"""
    if user_type_id == user_type.ADMIN:
        return {'orgs': get_all_orgs()}
    elif user_type_id == user_type.TEACHER:
        return {}
    elif user_type_id == user_type.PUPIL:
        return {}
    return {}
