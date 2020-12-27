from src.apps.core.admin.models import BaseModelAdmin


class UserLogAdmin(BaseModelAdmin):
    list_display = ('id', 'log_user', 'text', 'created_at')
