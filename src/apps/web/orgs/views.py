from django.shortcuts import render, redirect

from src.apps.core.api import BaseDeleteView, BaseCreateOrChangeView
from src.apps.core.service import create_org, change_org, get_org_by_id, delete_org
from src.apps.core.models import Organization
from src.apps.users.service import set_org
from django.views import View

from src.apps.users.models import User, user_type


class AllOrgsView(View):

    @staticmethod
    def get(request):
        data = {
            'user': request.user,
            'orgs': Organization.objects.all(),
            'admins': User.objects.filter(status_id=user_type.ADMIN)
        }
        return render(request, 'organization_list.html', context=data)


class CreateOrgView(View):

    @staticmethod
    def get(request):
        return render(request, 'organization_create_or_change.html')

    @staticmethod
    def post(request):
        name = request.POST.get('name')
        create_org(name)
        return redirect('/organizations/all')


class ChangeOrgView(View):

    @staticmethod
    def get(request, org_id):
        org = get_org_by_id(org_id)
        return render(request, 'organization_create_or_change.html', context={'org': org})

    @staticmethod
    def post(request, org_id):
        name = request.POST.get('name')
        change_org(org_id, name)
        return redirect('/organizations/all')


class DeleteOrgView(BaseDeleteView):
    model = Organization


class CreateOrChangeView(BaseCreateOrChangeView):
    model = Organization
    _fields = {
        'id': {
            'type': BaseCreateOrChangeView.FieldTypeEnumerate.STR,
            'validator': lambda val: int(val) > 0
        },
        'name': {
            'type': BaseCreateOrChangeView.FieldTypeEnumerate.STR,
            'required': True
        }
    }

    def extra_post(self, request):
        admins_id = request.data.getlist('admins_id[]')
        for u in User.objects.filter(id__in=admins_id):
            print('u {}'.format(u))
            set_org(u, self.obj)
