from django.test import TestCase
from django.urls import reverse_lazy

from .models import CategoryBrand, CategoryColor, CategoryGender, CategorySize, Shoes


class HomePageTests(TestCase):
    def test_view(self):
        path = reverse_lazy("shoes:home")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shoes/index.html")


class ListPairViewTests(TestCase):
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
