from src.apps.core.apps import BaseConfig


class Config(BaseConfig):
    name = 'src.apps.users'
    label = 'users'
    verbose_name = 'Пользователи'
    models_to_check = {
        'usertype': ['check_and_create_user_types']
    }
