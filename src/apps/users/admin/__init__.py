from django.contrib.admin import site
from django.contrib.auth.models import Group
from ..models import User, RegistrationRequest, UserType, UserLog
from .models import UserAdmin, UserLogAdmin


site.register(User, UserAdmin)
site.register(RegistrationRequest)
site.register(UserType)
site.register(UserLog, UserLogAdmin)
site.unregister(Group)
