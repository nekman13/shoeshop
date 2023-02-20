from django import template
from django.db.models import Count
from shoes.models import CategoryBrand, CategoryGender

register = template.Library()


@register.inclusion_tag("shoes/nav_list_category_brand.html")
def show_brand_categories():
    categories_brand = CategoryBrand.objects.annotate(cnt=Count("shoes")).filter(
        cnt__gt=0
    )

    return {"categories_brand": categories_brand}


@register.inclusion_tag("shoes/filter_list_category_gender.html")
def filter_show_gender_categories():
    categories_gender = CategoryGender.objects.filter(pk__lt=3)

    return {"categories_gender": categories_gender}
