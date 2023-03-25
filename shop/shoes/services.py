from django.contrib.auth.decorators import login_required
from django.db.models import Max, Min, Q
from django.shortcuts import redirect

from shoes.models import (Basket, CategoryBrand, CategoryColor, CategoryGender,
                          CategorySize, Shoes)


@login_required()
def basket_add(request, shoes_id):
    shoes = Shoes.objects.get(pk=shoes_id)
    baskets = Basket.objects.filter(user=request.user, shoes=shoes)

    if not baskets.exists():
        Basket.objects.create(user=request.user, shoes=shoes, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return redirect(request.META.get("HTTP_REFERER"))


@login_required()
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return redirect(request.META.get("HTTP_REFERER"))


def filter_pairs(
    min_price,
    max_price,
    lst_category_brand,
    lst_category_color,
    lst_category_gender,
    lst_category_size,
):
    if lst_category_brand == []:
        lst_category_brand = CategoryBrand.objects.values("pk")
    if lst_category_color == []:
        lst_category_color = CategoryColor.objects.values("pk")
    if lst_category_gender == []:
        lst_category_gender = CategoryGender.objects.values("pk")
    if lst_category_size == []:
        lst_category_size = CategorySize.objects.values("pk")
    if min_price == "":
        min_price = Shoes.objects.aggregate(Min("price"))["price__min"]
    if max_price == "":
        max_price = Shoes.objects.aggregate(Max("price"))["price__max"]

    queryset = Shoes.objects.filter(
        Q(category_brand_id__in=lst_category_brand)
        & Q(category_color_id__in=lst_category_color)
        & Q(category_gender_id__in=lst_category_gender)
        & Q(category_size__in=lst_category_size)
        & Q(price__gte=min_price)
        & Q(price__lte=max_price)
    ).distinct()

    return queryset


def search_request_filter(search_request):
    if search_request:
        return Shoes.objects.filter(
            Q(brand__icontains=search_request)
            | Q(model__icontains=search_request)
            | Q(color__icontains=search_request)
        )
    else:
        return Shoes.objects.all()
