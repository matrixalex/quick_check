from django.contrib.admin import site
from ..models import Organization, StudyClass, Document


site.register(Organization)
site.register(StudyClass)
site.register(Document)
