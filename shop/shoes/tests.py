from django.test import TestCase
from django.urls import reverse_lazy

from .models import (CategoryBrand, CategoryColor, CategoryGender,
                     CategorySize, Shoes)


class HomePageTestCase(TestCase):
    def test_view(self):
        path = reverse_lazy("shoes:home")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shoes/index.html")


class ListPairViewTestCase(TestCase):
    fixtures = [
        "shoes.json",
        "brands.json",
        "colors.json",
        "sizes.json",
        "genders.json",
    ]

    def setUp(self):
        self.shoes = Shoes.objects.all()

    def test_view(self):
        path = reverse_lazy("shoes:list_pair_view")
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shoes/list_pairs_view.html")
        self.assertEqual(response.context["title"], "Каталог")
        self.assertEqual(list(response.context["all_pair"]), list(self.shoes))
        self.assertEqual(
            list(response.context["brands"]), list(CategoryBrand.objects.all())
        )
        self.assertEqual(
            list(response.context["colors"]), list(CategoryColor.objects.all())
        )
        self.assertEqual(
            list(response.context["genders"]), list(CategoryGender.objects.all())
        )
        self.assertEqual(
            list(response.context["sizes"]), list(CategorySize.objects.all())
        )


class OnePairViewTestCase(TestCase):
    fixtures = [
        "shoes.json",
        "brands.json",
        "colors.json",
        "sizes.json",
        "genders.json",
    ]

    def setUp(self):
        self.path = reverse_lazy("shoes:one_pair_view", args="5")

    def test_view(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shoes/one_pair_view.html")


class GetCategoryBrandTestCase(TestCase):
    fixtures = [
        "shoes.json",
        "brands.json",
        "colors.json",
        "sizes.json",
        "genders.json",
    ]

    def setUp(self):
        self.path = reverse_lazy("shoes:category_brand", args="1")

    def test_view(self):
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, "shoes/list_pairs_view.html")
        self.assertEqual(response.status_code, 200)

    def test_filter(self):
        response = self.client.get(self.path)

        only_nike_pairs = CategoryBrand.objects.get(pk=1).shoes_set.all()
        self.assertEqual(
            list(response.context["shoes"]), list(only_nike_pairs)[:8]
        )  # Что он действительно фильтрует по брендам


class GetCategoryGenderTestCase(TestCase):
    fixtures = [
        "shoes.json",
        "brands.json",
        "colors.json",
        "sizes.json",
        "genders.json",
    ]

    def setUp(self):
        self.path = reverse_lazy("shoes:category_gender", args="1")

    def test_view(self):
        response = self.client.get(self.path)

        self.assertTemplateUsed(response, "shoes/list_pairs_view.html")
        self.assertEqual(response.status_code, 200)

    def test_filter(self):
        response = self.client.get(self.path)

        man_pairs = Shoes.objects.filter(category_gender_id__in=(1, 3))
        self.assertEqual(list(response.context["shoes"]), list(man_pairs)[:8])


class FilterViewTestCase(TestCase):
    fixtures = [
        "shoes.json",
        "brands.json",
        "colors.json",
        "sizes.json",
        "genders.json",
    ]

    def setUp(self):
        self.data = {
            # "filter": ""
        }
        self.path = reverse_lazy("shoes:list_pair_view")

    def test_view(self):
        response = self.client.get(self.path)

        self.assertTemplateUsed(response, "shoes/list_pairs_view.html")
        self.assertEqual(response.status_code, 200)


class SearchTestCase(TestCase):
    fixtures = [
        "shoes.json",
        "brands.json",
        "colors.json",
        "sizes.json",
        "genders.json",
    ]

    def setUp(self):
        self.path = reverse_lazy("shoes:search")
        self.data = {"request_search": "adidas"}

    def test_view(self):
        response = self.client.get(self.path)

        self.assertTemplateUsed(response, "shoes/list_pairs_view.html")
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = self.client.get(self.path, self.data)

        self.assertTemplateUsed(response, "shoes/list_pairs_view.html")
        self.assertEqual(response.status_code, 200)

        adidas_pairs = Shoes.objects.filter(category_brand_id=2)
        self.assertEqual(list(response.context["shoes"]), list(adidas_pairs))
