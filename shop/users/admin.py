from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email"]
    search_fields = ["username", "email"]
    verbose_name_plural = "Пользователи"
    verbose_name = "Пользователь"
