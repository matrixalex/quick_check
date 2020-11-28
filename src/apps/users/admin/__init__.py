from django.contrib.admin import site
from django.contrib.auth.models import Group
from ..models import User, RegistrationRequest
from .models import UserAdmin


site.register(User, UserAdmin)
site.register(RegistrationRequest)
site.unregister(Group)
