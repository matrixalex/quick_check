from src.apps.core.admin.models import BaseModelAdmin
from src.apps.users.models import User, user_type


class StudyClassAdmin(BaseModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "teachers":
            kwargs["queryset"] = User.objects.filter(status=user_type.TEACHER)
        return super(StudyClassAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
