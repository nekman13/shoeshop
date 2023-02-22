from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import CommonMixin
from shoes.models import Basket

from .forms import UserChangeProfileForm, UserLoginForm, UserRegisterForm
from .models import EmailVerification, User


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
    success_message = "Перейдите по ссылке на вашей почте!"
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


class EmailVerificationView(CommonMixin, TemplateView):
    title = "Подтверждение почты"
    template_name = "users/email_verification.html"

    def get(self, request, *args, **kwargs):
        code = kwargs["code"]
        user = User.objects.get(email=kwargs["email"])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verified = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy("shoes:home"))
