from django.shortcuts import render, redirect
from src.apps.core.service import create_org, change_org, get_org_by_id, delete_org
from src.apps.core.models import Organization
from django.views import View


class AllOrgsView(View):

    @staticmethod
    def get(request):
        data = {'user': request.user, 'orgs': Organization.objects.all()}
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


class DeleteOrgView(View):

    @staticmethod
    def get(request, org_id):
        delete_org(org_id)
        return redirect('/organizations/all')
