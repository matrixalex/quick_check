from django.apps import AppConfig


class Config(AppConfig):
    name = 'src.apps.users'
    label = 'users'

    def ready(self):
        self.verbose_name = 'Пользователи'
