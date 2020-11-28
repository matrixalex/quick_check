from django.apps import AppConfig


class Config(AppConfig):
    name = 'src.apps.core'
    label = 'core'

    def ready(self):
        self.verbose_name = 'Ядро'
