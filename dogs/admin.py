from django.contrib import admin

from dogs.models import Breed, Dog


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    """
    Регистрация модели Breed в административном интерфейсе
    """
    list_display = ('pk', 'name',)
    ordering = ('pk',)


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    """
    Регистрация модели Dog в административном интерфейсе
    """
    list_display = ('name', 'breed', 'owner',)
    list_filter = ('breed',)
    ordering = ('name',)
