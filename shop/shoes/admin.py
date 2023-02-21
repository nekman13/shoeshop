from django.contrib import admin

from .models import (Basket, CategoryBrand, CategoryColor, CategoryGender,
                     CategorySize, Shoes)


class ShoesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "brand",
        "model",
        "color",
        "price",
        "description",
        "realise_date",
        "update_date",
        "photo",
        "is_special",
        "category_brand",
        "category_color",
        "category_gender",
        "get_sizes",
    )
    list_display_links = ("id", "brand")
    search_fields = ("brend", "model")
    list_editable = ("is_special",)
    list_filter = ("is_special",)

    def get_sizes(self, obj):
        return "\n".join([cs.title_size for cs in obj.category_size.all()])


class CategoryAdminBrand(admin.ModelAdmin):
    list_display = ("id", "category_brand")
    list_display_links = ("id", "category_brand")
    search_fields = ("category_brand",)


class CategoryAdminColor(admin.ModelAdmin):
    list_display = ("id", "category_color")
    list_display_links = ("id", "category_color")
    search_fields = ("category_color",)


class CategoryAdminGender(admin.ModelAdmin):
    list_display = ("id", "category_gender")
    list_display_links = ("id", "category_gender")
    search_fields = ("category_gender",)


class CategoryAdminSize(admin.ModelAdmin):
    list_display = ("id", "title_size", "category_size")
    list_display_links = ("id", "category_size")


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = [
        "id",
        "user",
        "shoes",
    ]
    # list_display = (
    #     "id",
    #     "user",
    #     "shoes",
    # )
    # list_display_links = ("id", "user")


admin.site.register(Shoes, ShoesAdmin)
admin.site.register(CategoryBrand, CategoryAdminBrand)
admin.site.register(CategoryColor, CategoryAdminColor)
admin.site.register(CategoryGender, CategoryAdminGender)
admin.site.register(CategorySize, CategoryAdminSize)
