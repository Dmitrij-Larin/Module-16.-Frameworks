from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Настройка приложения, связанная с пользователями
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
