from django.contrib.admin import ModelAdmin
from ..actions import delete_selected


class BaseModelAdmin(ModelAdmin):

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(BaseModelAdmin, self).get_form(request, obj, change, **kwargs)
        form.current_user = request.user
        return form

    def get_actions(self, request):
        actions = super(BaseModelAdmin, self).get_actions(request)
        actions['delete_selected'] = (delete_selected, 'delete_selected', u'Удалить')
        return actions
