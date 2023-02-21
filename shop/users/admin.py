from django.contrib import admin

from shoes.admin import BasketAdmin

from .models import EmailVerification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email"]
    search_fields = ["username", "email"]
    inlines = [BasketAdmin]
    verbose_name_plural = "Пользователи"
    verbose_name = "Пользователь"


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ["code", "user", "expiration"]
    fields = ["user", "code", "created", "expiration"]
    readonly_fields = ["created"]
