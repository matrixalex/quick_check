from django.shortcuts import render, redirect

from src.apps.core.api import BaseDeleteView, BaseCreateOrChangeView
from src.apps.core.service import create_org, change_org, get_org_by_id, delete_org
from src.apps.core.models import Organization
from src.apps.homework.models import Homework, Question, QuestionAppeal
from src.apps.users.service import set_org
from django.views import View

from src.apps.users.models import User, user_type


class CreateOrChangeHomeworkView(BaseCreateOrChangeView):
    model = Homework
    _fields = {
        'name': {
            'type': BaseCreateOrChangeView.FieldTypeEnumerate.STR,
            'required': True
        },
        'description': {
            'type': BaseCreateOrChangeView.FieldTypeEnumerate.STR,
            'required': True
        },

    }


