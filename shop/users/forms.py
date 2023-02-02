from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)

from .models import User


class UserLoginForm(AuthenticationForm):
    """Класс формы аутентификации пользователя"""

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control py-4",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Пароль",
                "class": "form-control py-4",
            }
        )
    )

    class Meta:
        model = User
        fields = ("username", "password")


class UserRegisterForm(UserCreationForm):
    """Класс формы регистрации пользователя."""

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите имя",
                "class": "form-control py-4",
            }
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите фамилию",
                "class": "form-control py-4",
            }
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите имя пользователя",
                "class": "form-control py-4",
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Введите email",
                "class": "form-control py-4",
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Введите пароль",
                "class": "form-control py-4",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Подтвердите пароль",
                "class": "form-control py-4",
            }
        )
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )


class UserChangeProfileForm(UserChangeForm):
    """Класс для изменения профиля пользователя"""

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control py-4",
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control py-4",
            }
        )
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "custom-file-label"}), required=False
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control py-4",
                "readonly": True,
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control py-4",
                "readonly": True,
            }
        )
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "image", "username", "email"]
