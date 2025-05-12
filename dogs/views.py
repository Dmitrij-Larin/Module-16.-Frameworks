from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from dogs.forms import DogForm, DogParentForm, DogAdminForm
from dogs.models import Breed, Dog, DogParent
from dogs.services import send_views_mail
from users.models import UserRoles


def index(request):
    """
    Представление главной страницы
    """
    context = {
        'object_list': Breed.objects.all()[:3],
        'title': 'Питомник - Главная'
    }
    return render(request, 'dogs/index.html', context)


class BreedListView(LoginRequiredMixin, ListView):
    """
    Представление списка пород собак
    """
    model = Breed
    extra_context = {
        'title': "Все наши породы"
    }
    template_name = 'dogs/breeds.html'
    paginate_by = 3


class BreedSearchListView(LoginRequiredMixin, ListView):
    """
    Результат поискового запроса по породе собак
    """
    model = Breed
    template_name = 'dogs/breeds.html'
    extra_context = {
        'title': 'Результаты поискового запроса'
    }

    def get_queryset(self):
        """
        Получение списка объектов по определенному запросу
        """
        query = self.request.GET.get('q')
        print(query)
        object_list = Breed.objects.filter(
            Q(name__icontains=query)
        )
        return object_list


class DodBreedListView(LoginRequiredMixin, ListView):
    """
    Продставление списка собак определенной породы
    """
    model = Dog
    template_name = 'dogs/dogs.html'
    extra_context = {
        'title': 'Собаки выбранной породы'
    }

    def get_queryset(self):
        """
        Получение списка обЪектов
        """
        queryset = super().get_queryset().filter(breed_id=self.kwargs.get('pk'))
        return queryset


class DodListView(ListView):
    """
    Представление всех собак
    """
    model = Dog
    extra_context = {
        'title': 'Питомник - Все наши собаки',
    }
    template_name = 'dogs/dogs.html'
    paginate_by = 3

    def get_queryset(self):
        """
        Получение списка обЪектов
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class DogDeactivatedListView(LoginRequiredMixin, ListView):
    """
    Представление списка неактивных собак
    """
    model = Dog
    extra_context = {
        'title': 'Питомник - неактивные собаки'
    }
    template_name = 'dogs/dogs.html'

    def get_queryset(self):
        """
        Получение списка обЪектов
        """
        queryset = super().get_queryset()
        if self.request.user.role in [UserRoles.MODERATOR, UserRoles.ADMIN]:
            queryset = queryset.filter(is_active=False)
        if self.request.user.role == UserRoles.USER:
            queryset = queryset.filter(is_active=False, owner=self.request.user)
        return queryset


class DogSearchListView(LoginRequiredMixin, ListView):
    """
    Результаты поискового запроса по кличке собаки
    """
    model = Dog
    template_name = 'dogs/dogs.html'
    extra_context = {
        'title': 'Результаты поискового запроса'
    }

    def get_queryset(self):
        """
        Получение списка обЪектов
        """
        query = self.request.GET.get('q')
        print(query)
        object_list = Dog.objects.filter(
            Q(name__icontains=query), is_active=True,
        )
        return object_list


class DogCreateView(LoginRequiredMixin, CreateView):
    """
    Добавление (создание) собаки
    """
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    extra_context = {
        'title': 'Добавить собаку'
    }
    success_url = reverse_lazy('dogs:dogs_list')

    def form_valid(self, form):
        """
        Валидация формы, перед добавлением собаки
        """
        if self.request.user.role != UserRoles.USER:
            raise PermissionDenied()
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class DogDetailView(DetailView):
    """
    Представление подробной информации о собаке
    """
    model = Dog
    template_name = 'dogs/detail.html'

    def get_context_data(self, **kwargs):
        """
        Передача дополнительных параметров в контекст шаблона проекта
        """
        context_data = super().get_context_data(**kwargs)
        object_ = self.get_object()
        context_data['title'] = f'Подробная информация {object_}'
        dog_object_increase = get_object_or_404(Dog, pk=object_.pk)
        if object_.owner != self.request.user:
            dog_object_increase.views_count()
        if object_.owner:
            object_owner_email = object_.owner.email
            if dog_object_increase.views % 20 == 0 and dog_object_increase.views != 0:
                send_views_mail(dog_object_increase.name, object_owner_email, dog_object_increase.views)
        return context_data


class DogUpdateView(LoginRequiredMixin, UpdateView):
    """
    Изменение (обновление) собаки
    """
    model = Dog
    template_name = 'dogs/create_update.html'
    extra_context = {
        'title': 'Изменить собаку'
    }

    def get_success_url(self):
        """
        Перенаправление пользователя после успешного обновления объекта
        """
        return reverse('dogs:dog_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        """
        Проверка на соответствие владельца объекта текущему пользователю
        """
        self.object = super().get_object(queryset)
        # if self.object.owner != self.request.user and not self.request.user.is_staff:
        if self.object.owner != self.request.user and self.request.user.role != UserRoles.ADMIN:
            raise PermissionDenied()
        return self.object

    def get_form_class(self):
        """
        Выбор класса формы в зависимости от роли пользователя
        """
        dog_forms = {
            'admin': DogAdminForm,
            'moderator': DogForm,
            'user': DogForm
        }
        user_role = self.request.user.role
        dog_form_class = dog_forms[user_role]
        return dog_form_class

    def get_context_data(self, **kwargs):
        """
        Передача дополнительных параметров в контекст шаблона проекта
        """
        context_data = super().get_context_data(**kwargs)
        DogParentFormset = inlineformset_factory(Dog, DogParent, form=DogParentForm, extra=1)
        if self.request.method == 'POST':
            formset = DogParentFormset(self.request.POST, instance=self.object)
        else:
            formset = DogParentFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        """
        Валидация формы
        """
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class DogDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Удаление собаки
    """
    model = Dog
    template_name = 'dogs/delete.html'
    extra_context = {
        'title': 'Удалить собаку'
    }
    success_url = reverse_lazy('dogs:dogs_list')
    permission_required = 'dogs.delete_dog'
    permission_denied_message = "У Вас нет нужных прав для этого действия!"


def dog_toggle_activity(request, pk):
    """
    Переключения активности объекта "собака" в базе данных
    """
    dog_item = get_object_or_404(Dog, pk=pk)
    if dog_item.is_active:
        dog_item.is_active = False
    else:
        dog_item.is_active = True
    dog_item.save()
    return redirect(reverse('dogs:dogs_list'))
