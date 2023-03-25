from django.db.models import Q
from django.views.generic import DetailView, ListView

from common.views import CommonMixin

from .models import (
    Basket,
    CategoryBrand,
    CategoryColor,
    CategoryGender,
    CategorySize,
    Shoes,
)
from .services import filter_pairs, search_request_filter


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

    def get_queryset(self):
        return CategoryBrand.objects.get(
            pk=self.kwargs["category_brand_id"]
        ).shoes_set.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GetCategoryBrand, self).get_context_data(**kwargs)
        context[
            "title"
        ] = f'Пары: {CategoryBrand.objects.get(pk=self.kwargs["category_brand_id"])}'
        return context


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
        return queryset.filter(category_gender_id__in=(category_gender_id, 3))


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

        return filter_pairs(
            min_price,
            max_price,
            lst_category_brand,
            lst_category_color,
            lst_category_gender,
            lst_category_size,
        )


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
        context["shoes"] = search_request_filter(search_request)
        context["shoes_count"] = context["shoes"].count()
        return context
