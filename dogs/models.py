from django.db import models
from django.conf import settings

from users.models import NULLABLE


class Breed(models.Model):
    """
    Модель породы собаки
    """
    name = models.CharField(max_length=100, verbose_name='breed')
    description = models.CharField(max_length=1000, verbose_name='description', **NULLABLE)

    def __str__(self):
        """
        Представление модели в строковом виде
        """
        return f'{self.name}'

    class Meta:
        """
        Настройки параметров модели Breed
        """
        verbose_name = 'breed'
        verbose_name_plural = 'breeds'


class Dog(models.Model):
    """
    Модель собаки
    """
    name = models.CharField(max_length=150, verbose_name='Кличка')
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name='Порода')
    photo = models.ImageField(upload_to='dogs/', **NULLABLE, verbose_name='Изображение')
    birth_date = models.DateField(**NULLABLE, verbose_name='Дата рождения')
    is_active = models.BooleanField(default=True, verbose_name='Активность')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Хозяин')
    views = models.IntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        """
        Представление модели в строковом виде
        """
        return f'{self.name} ({self.breed})'

    class Meta:
        """
        Настройки параметров модели Dog
        """
        verbose_name = 'dog'
        verbose_name_plural = 'dogs'
        # abstract = True
        # app_label = 'dogs'
        # ordering = [-1]
        # permission = []
        # db_table = 'doggies'
        # get_latest_by = 'birth_date'

    def views_count(self):
        """
        Счётчик просмотров модели
        """
        self.views += 1
        self.save()


class DogParent(models.Model):
    """
    Модель собаки-родителя
    """
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, verbose_name='Кличка Родителя')
    category = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name='Порода Родителя')
    birth_date = models.DateField(**NULLABLE, verbose_name='Дата рождения Родителя')

    def __str__(self):
        """
        Представление модели в строковом виде
        """
        return f'{self.name} ({self.breed})'

    class Meta:
        """
        Настройки параметров модели DogParent
        """
        verbose_name = 'parent'
        verbose_name_plural = 'parents'
