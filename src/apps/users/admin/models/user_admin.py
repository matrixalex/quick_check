from src.apps.core.admin.models import BaseModelAdmin
from django import forms


class UserChangeForm(forms.ModelForm):
    password_new = forms.CharField(required=False)
    password_new_confirm = forms.CharField(required=False)

    class Meta:
        fields = '__all__'

    def save(self, commit=True, *args, **kwargs):
        user = super(UserChangeForm, self).save(commit=False)
        password_new = self.cleaned_data['password_new']
        password_new_confirm = self.cleaned_data['password_new_confirm']
        if password_new and password_new == password_new_confirm:
            user.set_password(password_new)
        user.save()
        return user


class UserAdmin(BaseModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'created_at', 'is_deleted')

    fieldsets = (
        ('Пользовательские данные', {'fields': ('first_name', 'last_name', 'middle_name', 'status', 'email')}),
        ('Права доступа', {'fields': ('user_permissions', 'is_staff', 'is_superuser')}),
        ('Изменение пароля', {'fields': ('password_new', 'password_new_confirm')})
    )

    form = UserChangeForm
    add_form = UserChangeForm

    def delete_model(self, request, obj):
        super(UserAdmin, self).delete_model(request, obj)
