from django.shortcuts import render

from src.apps.core.api import BaseDeleteView, BaseCreateOrChangeView
from src.apps.core.service import get_study_classes
from src.apps.core.models import StudyClass
from django.views import View

from src.apps.users.models import User, user_type


class ListView(View):

    @staticmethod
    def get(request):
        data = {
            'user': request.user,
            'study_classes': get_study_classes(request.user.org),
            'teachers': User.objects.filter(org=request.user.org, status=user_type.TEACHER),
            'pupils': User.objects.filter(study_class__org=request.user.org, status=user_type.PUPIL),
            'org': request.user.org
        }

        return render(request, 'study_classes.html', context=data)


class DeleteView(BaseDeleteView):
    model = StudyClass


class CreateOrChangeView(BaseCreateOrChangeView):
    model = StudyClass
    _fields = {
        'id': {
            'type': BaseCreateOrChangeView.FieldTypeEnumerate.STR,
            'validator': lambda val: int(val) > 0
        },
        'name': {
            'type': BaseCreateOrChangeView.FieldTypeEnumerate.STR,
            'required': True
        },
        'org_id': {
            'type': BaseCreateOrChangeView.FieldTypeEnumerate.INT,
            'required': True
        }
    }

    def extra_post(self, request):
        teachers_id = request.data.getlist('teachers_id[]')
        self.obj.teachers.clear()
        for u in User.objects.filter(id__in=teachers_id):
            self.obj.teachers.add(u)
        pupils_id = request.data.getlist('pupils_id[]')
        User.objects.filter(id__in=pupils_id).update(study_class_id=self.obj.id)

