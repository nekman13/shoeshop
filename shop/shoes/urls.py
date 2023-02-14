from django.contrib.auth.decorators import login_required
from django.urls import path

from .services import basket_add, basket_remove
from .views import *

app_name = "shoes"

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("list_pair_view/", ListPairView.as_view(), name="list_pair_view"),
    path("one_pair_view/<int:pk>", OnePairView.as_view(), name="one_pair_view"),
    path(
        "category_brand/<int:category_brand_id>/",
        GetCategoryBrand.as_view(),
        name="category_brand",
    ),
    path(
        "category_gender/<int:category_gender_id>",
        GetCategoryGender.as_view(),
        name="category_gender",
    ),
    path("filter/", FilterView.as_view(), name="filter"),
    path("search/", Search.as_view(), name="search"),
    path("baskets/add/<int:shoes_id>/", basket_add, name="basket_add"),
    path(
        "baskets/remove/<int:basket_id>/",
        basket_remove,
        name="basket_remove",
    ),
]
