from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from cloudapp.models import UserActivityLog
from cloud_django_project.forms import UserRegistrationForm

class RegisterUserTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register_user')  # replace 'register_user' with the actual url name for the register_user view

    def test_register_user_valid_data(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # 302 status code means redirect, which is the expected behavior
        self.assertTrue(UserActivityLog.objects.filter(username='testuser', activity='register').exists())

    def test_register_user_invalid_data(self):
        response = self.client.post(self.register_url, {
            'username': '',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertEqual(response.status_code, 200)  # 200 status code means the form was not valid and the user is presented with the form again
        self.assertFormError(response, 'form', 'username', 'This field is required.')

    def test_register_user_username_already_exists(self):
        UserRegistrationForm.objects.create_user('testuser', 'testpassword123')
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')