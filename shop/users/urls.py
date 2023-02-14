from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import UserLoginView, UserLogoutView, UserProfileView, UserRegisterView

app_name = "users"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("logout/", login_required(UserLogoutView.as_view()), name="logout"),
    path(
        "profile/<int:pk>/", login_required(UserProfileView.as_view()), name="profile"
    ),
]
