import random
import string

from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy

from users.models import User
from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserPasswordChangeForm, UserForm
from users.services import send_new_password, send_register_email


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:user_login')
    template_name = 'users/user_register.html'
    extra_context = {
        'title': 'Регистрация пользователя'
    }

# def user_register_view(request):
#     form = UserRegisterForm(request.POST)
#     if request.method == "POST":
#         if form.is_valid():
#             new_user = form.save()
#             new_user.set_password(form.cleaned_data['password'])
#             new_user.save()
#             send_register_email(new_user.email)
#             return HttpResponseRedirect(reverse('users:user_login'))
#     context = {
#         'title': 'Создать аккаунт',
#         'form': UserRegisterForm
#     }
#     return render(request, 'users/user_register.html', context=context)


class UserLoginView(LoginView):
    template_name = 'users/user_login.html'
    form_class = UserLoginForm
    extra_context = {
        'title': 'Вход в аккаунт'
    }


# def user_login_view(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(email=cd['email'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponseRedirect(reverse('dogs:index'))
#             return HttpResponse('Вы не можете войти на наш ресурс (ошибка пароля, нет аккаунта или Вы забанены)')
#     context = {
#             'title': 'Вход в аккаунт',
#             'form': UserLoginForm
#     }
#     return render(request, 'users/user_login.html', context=context)


class UserProfileView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_profile_read_only.html'
    extra_context = {
        'title': 'Ваш профиль'
    }

    def get_object(self, queryset=None):
        return self.request.user

# @login_required
# def user_profile_view(request):
#     user_object = request.user
#     context = {
#         'title': f'Ваш профиль {user_object.first_name} {user_object.last_name}'
#     }
#     return render(request, 'users/user_profile_read_only.html', context)


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users:user_profile')
    extra_context = {
        'title': 'Обновить профиль'
    }

    def get_object(self, queryset=None):
        return self.request.user


# @login_required
# def user_update_view(request):
#     user_object = request.user
#     if request.method == 'POST':
#         form = UserUpdateForm(request.POST, request.FILES, instance=user_object)
#         if form.is_valid():
#             user_object = form.save()
#             user_object.save()
#             return HttpResponseRedirect(reverse('users:user_profile'))
#     context = {
#         'object': user_object,
#         'title': f'Изменить профиль {user_object.first_name} {user_object.last_name}',
#         'form': UserUpdateForm(instance=user_object),
#     }
#     return render(request, 'users/user_update.html', context)


class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/user_change_password.html'
    success_url = reverse_lazy('users:user_profile')
    extra_context = {
        'title': 'Изменение пароля'
    }


# @login_required
# def user_change_password_view(request):
#     user_object = request.user
#     form = UserPasswordChangeForm(user_object, request.POST)
#     if request.method == 'POST':
#         if form.is_valid():
#             user_object = form.save()
#             update_session_auth_hash(request, user_object)
#             messages.success(request, 'Пароль был успешно изменён!')
#             return HttpResponseRedirect(reverse('users:user_profile'))
#         messages.error(request, 'Не удалось изменить пароль!')
#     context = {
#         'form': form
#     }
#     return render(request, 'users/user_change_password.html', context)


class UserLogoutView(LogoutView):
    template_name = 'users/user_logout.html'
    extra_context = {
        'title': 'Выход из аккаунта'
    }

# def user_logout_view(request):
#     logout(request)
#     return redirect('dogs:index')

@login_required
def user_generate_new_password_view(request):
    new_password = ''.join(random.sample((string.ascii_letters + string.digits), 12))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('dogs:index'))


