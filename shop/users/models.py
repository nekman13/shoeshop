from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""

    image = models.ImageField(upload_to="users_images", null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class EmailVerification(models.Model):
    """Подтверждение почты"""

    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f"Подтверждение для {self.user}"

    def send_verification_email(self):
        send_mail(
            "Подтверждение почты",
            f"Подтверждение почты для {self.user}",
            "from@mail.ru",
            [self.user.email],
            fail_silently=False,
        )
