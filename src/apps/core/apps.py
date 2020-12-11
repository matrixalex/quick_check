from django.apps import AppConfig
from src.quick_check.settings import NEED_CHECK_DATABASE


class BaseConfig(AppConfig):
    """
    Базовый класс конфига приложения, реализует метод check_database, который запускает кастомные методы проверки БД
    Вид словаря для проверки: {'model_name': ['method1', 'method2']}
    """
    models_to_check = {}

    def check_database(self):
        if NEED_CHECK_DATABASE:
            for model_name, methods_to_check in self.models_to_check.items():
                model = AppConfig.get_model(self, model_name)
                for method in methods_to_check:
                    try:
                        # Необходимо обеспечить классовый метод без параметров, лень расширять
                        getattr(model, method)()
                    except AttributeError:
                        print('model {} has no check method {}, skipping'.format(model, method))

    def ready(self):
        self.check_database()


class Config(BaseConfig):
    name = 'src.apps.core'
    label = 'core'
    verbose_name = 'Ядро'
