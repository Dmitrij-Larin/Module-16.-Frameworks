from django.contrib import admin

from reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Review
    """
    list_display = ('title', 'dog', 'author', 'created', 'sign_of_review',)
    ordering = ('created',)
    list_filter = ('dog', 'author',)
