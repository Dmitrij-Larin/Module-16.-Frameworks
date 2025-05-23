import datetime

from django import forms

from dogs.models import Dog, DogParent
from users.forms import StyleFromMixin


class DogForm(StyleFromMixin, forms.ModelForm):
    """
    Класс формы DogForm, использующий ModelForm
    """
    class Meta:
        """
        Класс с настройками для модели Dog
        """
        model = Dog
        exclude = ('owner', 'is_active', 'views',)

    def clean_birth_date(self):
        """
        Валидация поля 'birth_date'
        """
        cleaned_data = self.cleaned_data['birth_date']
        if cleaned_data:
            now_year = datetime.datetime.now().year
            if now_year - cleaned_data.year > 35:
                raise forms.ValidationError('Собака должна быть моложе 35 лет')
        return cleaned_data


class DogAdminForm(DogForm):
    """
    Класс, предназначенный для работы в административной части приложения
    """
    class Meta:
        """
        Класс с настройками для модели Dog
        """
        model = Dog
        exclude = ('is_active',)

    # def clean_birth_date(self):
    #     cleaned_birth_date = super().clean_birth_date()
    #     return cleaned_birth_date


class DogParentForm(StyleFromMixin, forms.ModelForm):
    """
    Класс формы DogParentForm, использующий ModelForm
    """
    class Meta:
        """
        Класс с настройками для модели DogParent
        """
        model = DogParent
        fields = '__all__'
