import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class Shoes(models.Model):
    """Модель пар обуви"""

    brand = models.CharField(max_length=50, verbose_name="Бренд")
    model = models.CharField(max_length=50, verbose_name="Модель")
    color = models.CharField(max_length=50, verbose_name="Расцветка")
    price = models.IntegerField(verbose_name="Стоимость")
    description = models.TextField(blank=True, verbose_name="Описание")
    realise_date = models.IntegerField(verbose_name="Дата релиза")
    update_date = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего обновления"
    )
    photo = models.ImageField(
        blank=True, upload_to="photos/%Y/%m/%d", verbose_name="Фото"
    )
    is_special = models.BooleanField(default=False, verbose_name="Эксклюзивность")
    stripe_shoes_price_id = models.CharField(max_length=128, null=True, blank=True)
    category_brand = models.ForeignKey(
        "CategoryBrand",
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Категория бренд",
    )
    category_color = models.ForeignKey(
        "CategoryColor",
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Категория цвет",
    )
    category_gender = models.ForeignKey(
        "CategoryGender",
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Категория пол",
    )
    category_size = models.ManyToManyField(
        "CategorySize", blank=True, verbose_name="Категория размеров"
    )

    def __str__(self):
        return self.brand

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.stripe_shoes_price_id:
            stripe_shoes_price = self.create_stripe_shoes_price()
            self.stripe_shoes_price_id = stripe_shoes_price["id"]

        super(Shoes, self).save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )

    def create_stripe_shoes_price(self):
        stripe_shoes = stripe.Product.create(
            name=f"{self.brand} {self.model} {self.color}"
        )
        stripe_shoes_price = stripe.Price.create(
            product=stripe_shoes["id"],
            unit_amount=round(self.price * 100),
            currency="rub",
        )
        return stripe_shoes_price

    class Meta:
        verbose_name = "Пары"
        verbose_name_plural = "Пары"


class CategoryBrand(models.Model):
    """Модель категории бренда"""

    category_brand = models.CharField(
        max_length=100, db_index=True, verbose_name="Категория бренд"
    )

    def __str__(self):
        return self.category_brand

    class Meta:
        verbose_name = "Категория бренд"
        verbose_name_plural = "Категории бренда"


class CategoryColor(models.Model):
    """Модель категории цвета"""

    category_color = models.CharField(max_length=50, verbose_name="Цвет")

    def __str__(self):
        return self.category_color

    class Meta:
        verbose_name = "Категория цвет"
        verbose_name_plural = "Категории цвета"


class CategoryGender(models.Model):
    """Модель категории пола"""

    category_gender = models.CharField(max_length=50, verbose_name="Пол")

    def __str__(self):
        return self.category_gender

    class Meta:
        verbose_name = "Категория пол"
        verbose_name_plural = "Категории пола"


class CategorySize(models.Model):
    """ "Модель категории размеров"""

    title_size = models.CharField(
        max_length=50, blank=True, verbose_name="Заголовок размеров"
    )
    category_size = models.IntegerField(verbose_name="Размер")

    def __str__(self):
        return self.title_size

    class Meta:
        verbose_name = "Категория размеров"
        verbose_name_plural = "Категории размеров"


class BasketQuerySet(models.QuerySet):
    """Класс для реализации методов подсчета общей стоимости корзины и количества товаров"""

    def total_sum_price(self):  # возвращает общую стоимость корзины
        return sum(basket.sum_price() for basket in self)

    def total_quantity(self):  # возвращает количество товаров в корзине
        return sum(basket.quantity for basket in self)

    def get_stripe_shoes(self):
        line_items = []
        for basket in self:
            item = {
                "price": basket.shoes.stripe_shoes_price_id,
                "quantity": basket.quantity,
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    """Модель корзины"""

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    shoes = models.ForeignKey(to=Shoes, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(verbose_name="Количество")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f" Корзина пользователя - {self.user.username} с {self.shoes.model}"

    def de_json(self):
        basket_item = {
            "product_name": f"{self.shoes.brand} {self.shoes.model} {self.shoes.color}",
            "quantity": self.quantity,
            "price": float(self.shoes.price),
            "summ": float(self.sum_price()),
        }
        return basket_item

    def sum_price(self):
        return self.shoes.price * self.quantity
