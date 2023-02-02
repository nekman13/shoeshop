from django.test import TestCase
from django.urls import reverse_lazy
from users.models import User


class UserRegistrationTestCase(TestCase):
    """Класс для тестирования регистрации пользователя"""

    def setUp(self):
        self.data = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "test",
            "email": "nnheo@example.com",
            "password1": "12345678Test",
            "password2": "12345678Test",
        }
        self.path = reverse_lazy("users:register")

    def test_user_registration_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")

    def test_user_registration_post_success(self):
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users:login"))
        self.assertTrue(User.objects.filter(username=self.data["username"]).exists)

    def test_user_registration_post_errors(self):
        username = self.data["username"]
        user = User.objects.create(username=username)

        response = self.client.post(self.path, self.data)
        self.assertContains(response, "Пользователь с таким именем уже существует.")
        self.assertEqual(response.status_code, 200)
