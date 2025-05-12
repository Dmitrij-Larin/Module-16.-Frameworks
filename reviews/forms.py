from django import forms
from reviews.models import Review
from users.forms import StyleFromMixin


class ReviewForm(StyleFromMixin, forms.ModelForm):
    """
    Форма модели отзывов (Reviews)
    """
    title = forms.CharField(max_length=150, label='Заголовок')
    content = forms.TextInput()
    slug = forms.SlugField(max_length=20, initial='temp_slug', widget=forms.HiddenInput())

    class Meta:
        """
        Класс с настройками для модели Review
        """
        model = Review
        fields = ('dog', 'title', 'content', 'slug',)
