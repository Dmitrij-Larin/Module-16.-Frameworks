from django.http import HttpResponseForbidden
from django.shortcuts import reverse, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied

from reviews.models import Review
from reviews.forms import ReviewForm
from users.models import UserRoles
from reviews.utils import slug_generator


class ReviewListView(ListView):
    """
    Список всех отзывов
    """
    model = Review
    extra_context = {
        'title': "Все отзывы"
    }
    template_name = 'reviews/reviews.html'
    paginate_by = 2

    def get_queryset(self):
        """
        Получение списка объектов по определенному запросу
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_review=True)
        return queryset


class ReviewDeactivatedListView(ListView):
    """
    Список неактивных отзывов
    """
    model = Review
    extra_context = {
        'title': "Неактивные отзывы"
    }
    template_name = 'reviews/reviews.html'
    paginate_by = 2

    def get_queryset(self):
        """
        Получение списка объектов по определенному запросу
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_review=False)
        return queryset


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """
    Создание отзыва
    """
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/create_update.html'
    extra_context = {
        'title': "Написать отзыв"
    }

    def form_valid(self, form):
        """
        Валидация формы пользователя, пишущего отзыв
        """
        if self.request.user.role not in [UserRoles.USER]:
            return HttpResponseForbidden
        self.object = form.save()
        print(self.object.slug)
        if self.object.slug == 'temp_slug':
            self.object.slug = slug_generator()
            print(self.object.slug)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ReviewDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр отзыва
    """
    model = Review
    template_name = 'reviews/detail.html'
    extra_context = {
        'title': "Просмотр отзыва"
    }


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    """
    Обновление (изменение) отзыва
    """
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/create_update.html'
    extra_context = {
        'title': "Изменить отзыв"
    }

    def get_success_url(self):
        """
        Перенаправление пользователя после успешного обновления объекта
        """
        return reverse('reviews:review_detail', args=[self.kwargs.get('slug')])

    def get_object(self, queryset=None):
        """
        Проверка на соответствие пользователю к текущему отзыву
        """
        self.object = super().get_object(queryset=queryset)
        if self.object.author != self.request.user and self.request.user not in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            raise PermissionDenied()
        return self.object


class ReviewDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Удаление отзыва
    """
    model = Review
    template_name = 'reviews/delete.html'
    permission_required = 'reviews.delete_review'

    def get_success_url(self):
        """
        Перенаправление пользователя после успешного обновления объекта
        """
        return reverse('reviews:reviews_list')


def review_toggle_activity(request, slug):
    """
    Переключения активности объекта "отзыв" в базе данных
    """
    review_item = get_object_or_404(Review, slug=slug)
    if review_item.sign_of_review:
        review_item.sign_of_review = False
        review_item.save()
        return redirect(reverse('reviews:reviews_deactivated'))
    else:
        review_item.sign_of_review = True
        review_item.save()
        return redirect(reverse('reviews:reviews_list'))
