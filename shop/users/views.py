from common.views import CommonMixin
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView
from shoes.models import Basket

from .forms import UserChangeProfileForm, UserLoginForm, UserRegisterForm
from .models import User


class UserLoginView(CommonMixin, SuccessMessageMixin, LoginView):
    """Класс для авторизации пользователя"""

    model = User
    template_name = "users/login.html"
    form_class = UserLoginForm
    title = "Авторизация"
    # success_message = 'Вы успешно авторизовались!'


class UserRegisterView(CommonMixin, SuccessMessageMixin, CreateView):
    """Класс для регистрации пользователя"""

    model = User
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")
    success_message = "Вы успешно зарегистрировались!"
    title = "Регистрация"


class UserLogoutView(CommonMixin, SuccessMessageMixin, View):
    """Класс для выхода из профиля"""

    # success_message = 'Вы успешно вышли из профиля!'
    title = "Выход"

    def get(self, request):
        logout(request)
        return redirect(reverse_lazy("shoes:home"))


class UserProfileView(CommonMixin, UpdateView):
    """Класс для редактирования профиля пользователя"""

    model = User
    template_name = "users/profile.html"
    form_class = UserChangeProfileForm
    success_url = reverse_lazy("users:profile")
    title = "Личный кабинет"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["baskets"] = Basket.objects.filter(user=self.request.user)
        return context

    def get_success_url(self):
        return reverse_lazy("users:profile", args=[self.request.user.id])
