from django.db import models

from shoes.models import Basket
from users.models import User


class Order(models.Model):
    """Модель заказа"""

    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, "Создан"),
        (PAID, "Оплачен"),
        (ON_WAY, "В пути"),
        (DELIVERED, "Доставлен"),
    )

    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(max_length=100, verbose_name="Адрес электронной почты")
    address = models.CharField(max_length=256, verbose_name="Адрес")
    basket_history = models.JSONField(default=dict, verbose_name="Товары в корзине")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата оформления заказа"
    )
    status = models.SmallIntegerField(
        default=CREATED, choices=STATUSES, verbose_name="Статус заказа"
    )
    initiator = models.ForeignKey(
        to=User, on_delete=models.CASCADE, verbose_name="Заказчик"
    )

    def __str__(self):
        return f"Заказ #{self.id} {self.first_name} {self.last_name}"

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.initiator)
        self.status = self.PAID
        self.basket_history = {
            "payment_products": [basket.de_json() for basket in baskets],
            "total_sum": float(baskets.total_sum_price()),
        }
        baskets.delete()
        self.save()

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
