from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""

    image = models.ImageField(upload_to="users_images", null=True, blank=True)

    def __str__(self):
        return self.username
