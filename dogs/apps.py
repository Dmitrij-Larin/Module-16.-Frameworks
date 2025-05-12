from django.apps import AppConfig


class DogsConfig(AppConfig):
    """
    Конфигурация приложения, связанная с собаками
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dogs'
