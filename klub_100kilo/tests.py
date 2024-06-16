from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from klub_100kilo.models import Users, Reservations, MeasurementsGoals
from klub_100kilo.views import hero_page, main_page
from klub_100kilo.forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model


# Views tests

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testpassword'
        )
        self.test_user.save()

        self.user = Users.objects.create(
            mail=self.test_user.email,
            password=self.test_user.password,
            first_name='Test',
            last_name='User',
            phone_number='123456789',
            role='User'
        )
        self.user.save()

        self.client.login(username='testuser', password='testpassword')

    def test_main_page_view(self):
        response = self.client.get(reverse('main_page'))
        self.assertEqual(response.status_code, 200)

    def test_account_view(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)

    def test_workouts_view(self):
        response = self.client.get(reverse('workouts'))
        self.assertEqual(response.status_code, 200)

    def test_goals_view(self):
        response = self.client.get(reverse('goals'))
        self.assertEqual(response.status_code, 200)


# Forms tests

class FormTestCase(TestCase):
    def test_register_form_valid(self):
        form = RegisterForm(data={
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '123456789',
            'email': 'testuser@test.com',
            'password': 'testpassword1@'
        })
        self.assertTrue(form.is_valid())

    def test_login_form_valid(self):
        form = LoginForm(data={
            'email': 'testuser@test.com',
            'password': 'testpassword1@'
        })
        self.assertTrue(form.is_valid())


# urls tests

class UrlsTestCase(SimpleTestCase):
    def test_hero_page_url(self):
        url = reverse('hero_page')
        self.assertEqual(resolve(url).func, hero_page)

    def test_main_page_url(self):
        url = reverse('main_page')
        self.assertEqual(resolve(url).func, main_page)


# Models tests

class ModelTestCase(TestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testpassword'
        )
        self.test_user.save()

        self.user = Users.objects.create(
            mail=self.test_user.email,
            password=self.test_user.password,
            first_name='Test',
            last_name='User',
            phone_number='123456789',
            role='User'
        )
        self.user.save()

def test_user_creation(self):
    self.assertIsInstance(self.user, Users)
