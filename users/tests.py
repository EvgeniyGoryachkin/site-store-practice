from http import HTTPStatus
import django
from django.test import TestCase
from django.urls import reverse
from datetime import timedelta
from users.forms import UserRegistrationForm
from users.models import User, EmailVerification
from django.utils.timezone import now

django.setup()
class userregistrationviewtestcase(TestCase):


    def setUp(self):
        self.path = reverse('users:register')
        self.data = {
            'first_name': 'Жэка', 'last_name': 'Жопич',
            'username': 'zhopich5', 'email': 'dedline111@yandex.ru',
            'password1': 'zheNEK11223344!', 'password2': 'zheNEK11223344!'
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        context_data = response.context_data
        self.assertEqual(context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_post_success(self):
        username = self.data['username']
        response = self.client.post(self.path, self.data)
        if response.status_code == 200:
            print(response.context['form'].errors)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue((email_verification.exists()))
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() == timedelta(hours=48)).date()
        )

# Create your tests here.
