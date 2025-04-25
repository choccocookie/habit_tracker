from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from Users.models import User


class UserAuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('user-register')
        self.login_url = reverse('token-obtain-pair')

        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "phone": "1234567890",
            "сity": "Test City",
            "telegram_chat_id": "123456"
        }

    def test_user_registration(self):
        """Тест регистрации пользователя"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.user_data['email']).exists())

    def test_user_login(self):
        """Тест авторизации пользователя (получение JWT)"""
        # Регистрируем пользователя
        self.client.post(self.register_url, self.user_data)

        # Логинимся
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, login_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
