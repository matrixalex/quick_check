from src.apps.core.apps import BaseConfig


class Config(BaseConfig):
    name = 'src.apps.homework'
    label = 'homework'
    verbose_name = 'Домашние работы'

    models_to_check = {
        'marktype': ['check_default_marktype'],
        'criterion': ['check_default_criterion']
    }
