from django.contrib.admin import site
from ..models import Organization, StudyClass, Document
from .models import StudyClassAdmin, BaseModelAdmin

site.register(Organization, BaseModelAdmin)
site.register(StudyClass, StudyClassAdmin)
site.register(Document)
