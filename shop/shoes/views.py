from common.views import CommonMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Min, Q
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

from .models import (Basket, CategoryBrand, CategoryColor, CategoryGender,
                     CategorySize, Shoes)


class HomePage(CommonMixin, ListView):
    """Класс для вывода домашней страницы"""

    model = Shoes
    template_name = "shoes/index.html"
    context_object_name = "shoes"
    title = "Главная страница"


class ListPairView(CommonMixin, ListView):
    """Класс для вывода всего списка пар"""

    model = Shoes
    template_name = "shoes/list_pairs_view.html"
    context_object_name = "shoes"
    paginate_by = 8

    title = "Каталог"
    flag = "list"

    def get_queryset(self):
        return Shoes.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListPairView, self).get_context_data(**kwargs)
        context["brands"] = CategoryBrand.objects.all()
        context["colors"] = CategoryColor.objects.all()
        context["genders"] = CategoryGender.objects.all()
        context["sizes"] = CategorySize.objects.all()
        context["all_pair"] = Shoes.objects.all()

        return context


class OnePairView(DetailView):
    """Класс для подробного просмотра одной пары"""

    model = Shoes
    context_object_name = "one_pair"
    template_name = "shoes/one_pair_view.html"


class GetCategoryBrand(CommonMixin, ListView):
    """Класс для вывода списка пар, определенной категории бренда"""

    model = Shoes
    template_name = "shoes/list_pairs_view.html"
    context_object_name = "shoes"
    paginate_by = 8

    flag = "filter_brand"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GetCategoryBrand, self).get_context_data(**kwargs)
        context[
            "title"
        ] = f'Пары: {CategoryBrand.objects.get(pk=self.kwargs["category_brand_id"])}'
        context["shoes_brand"] = CategoryBrand.objects.get(
            pk=self.kwargs["category_brand_id"]
        )
        return context

    def get_queryset(self):
        return Shoes.objects.filter(
            category_brand_id=self.kwargs["category_brand_id"]
        ).select_related("category_brand")


class GetCategoryGender(CommonMixin, ListView):
    """Класс для вывода списка пар, определенной категории пола"""

    model = Shoes
    template_name = "shoes/list_pairs_view.html"
    context_object_name = "shoes"
    paginate_by = 8
    title = "Пары"
    flag = "filter_gender"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GetCategoryGender, self).get_context_data(**kwargs)
        context["gender"] = CategoryGender.objects.get(
            pk=self.kwargs["category_gender_id"]
        )

        return context

    def get_queryset(self):
        queryset = super(GetCategoryGender, self).get_queryset()
        category_gender_id = self.kwargs["category_gender_id"]
        return queryset.filter(
            Q(category_gender_id=category_gender_id) | Q(category_gender_id=3)
        )


class FilterView(CommonMixin, ListView):
    """Класс для вывода отфильтрованного запроса пользователя"""

    model = Shoes
    context_object_name = "shoes"
    template_name = "shoes/list_pairs_view.html"
    title = "Каталог"
    flag = "filter"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FilterView, self).get_context_data(**kwargs)
        context["brands"] = CategoryBrand.objects.all()
        context["colors"] = CategoryColor.objects.all()
        context["genders"] = CategoryGender.objects.all()
        context["sizes"] = CategorySize.objects.all()
        context["all_pair"] = Shoes.objects.all()
        return context

    def get_queryset(self):
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        lst_category_brand = self.request.GET.getlist("category_brand")
        lst_category_color = self.request.GET.getlist("category_color")
        lst_category_gender = self.request.GET.getlist("category_gender")
        lst_category_size = self.request.GET.getlist("category_size")

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

        return Shoes.objects.filter(
            Q(category_brand_id__in=lst_category_brand)
            & Q(category_color_id__in=lst_category_color)
            & Q(category_gender_id__in=lst_category_gender)
            & Q(category_size__in=lst_category_size)
            & Q(price__gte=min_price)
            & Q(price__lte=max_price)
        ).distinct()


class Search(CommonMixin, ListView):
    """Класс для вывода результатов поиска"""

    context_object_name = "shoes"
    template_name = "shoes/list_pairs_view.html"
    title = "Поиск"
    flag = "search"

    def get_queryset(self):
        return Shoes.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        search_request = self.request.GET.get("request_search", "")

        context = super(Search, self).get_context_data(**kwargs)
        context["request_search"] = self.request.GET.get("request_search")
        if search_request:
            context["shoes"] = Shoes.objects.filter(
                Q(brand__icontains=search_request)
                | Q(model__icontains=search_request)
                | Q(color__icontains=search_request)
            )
        else:
            context["shoes"] = Shoes.objects.all()

        return context

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
