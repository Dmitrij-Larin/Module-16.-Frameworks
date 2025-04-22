from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http.response import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from dogs.forms import DogForm, DogParentForm
from dogs.models import Breed, Dog, DogParent
from users.models import UserRoles

def index(request):
    context = {
        'object_list': Breed.objects.all()[:3],
        'title': 'Питомник - Главная'
    }
    return render(request, 'dogs/index.html', context)


class BreedListView(LoginRequiredMixin, ListView):
    model = Breed
    extra_context = {
        'title': "Все наши породы"
    }
    template_name = 'dogs/breeds.html'


class DodBreedListView(LoginRequiredMixin, ListView):
    model = Dog
    template_name = 'dogs/dogs.html'
    extra_context = {
        'title': 'Собаки выбранной породы'
    }

    def get_queryset(self):
        queryset = super().get_queryset().filter(breed_id=self.kwargs.get('pk'))
        return queryset


class DodListView(ListView):
    model = Dog
    extra_context = {
        'title': 'Питомник - Все наши собаки',
    }
    template_name = 'dogs/dogs.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class DogDeactivatedListView(LoginRequiredMixin, ListView):
    model = Dog
    extra_context = {
        'title': 'Питомник - неактивные собаки'
    }
    template_name = 'dogs/dogs.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role in [UserRoles.MODERATOR, UserRoles.ADMIN]:
            queryset = queryset.filter(is_active=False)
        if self.request.user.role == UserRoles.USER:
            queryset = queryset.filter(is_active=False, owner=self.request.user)
        return queryset


class DogCreateView(LoginRequiredMixin, CreateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    extra_context = {
        'title': 'Добавить собаку'
    }
    success_url = reverse_lazy('dogs:dogs_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class DogDetailView(DetailView):
    model = Dog
    template_name = 'dogs/detail.html'
    extra_context = {
        'title': 'Подробная информация'
    }


class DogUpdateView(LoginRequiredMixin, UpdateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    extra_context = {
        'title': 'Изменить собаку'
    }

    def get_success_url(self):
        return reverse('dogs:dog_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        DogParentFormset = inlineformset_factory(Dog, DogParent, form=DogParentForm, extra=1)
        if self.request.method == 'POST':
            formset = DogParentFormset(self.request.POST, instance=self.object)
        else:
            formset = DogParentFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class DogDeleteView(LoginRequiredMixin, DeleteView):
    model = Dog
    template_name = 'dogs/delete.html'
    extra_context = {
        'title': 'Удалить собаку'
    }
    success_url = reverse_lazy('dogs:dogs_list')


def dog_toggle_activity(request, pk):
    dog_item = get_object_or_404(Dog, pk=pk)
    if dog_item.is_active:
        dog_item.is_active = False
    else:
        dog_item.is_active = True
    dog_item.save()
    return redirect(reverse('dogs:dogs_list'))

