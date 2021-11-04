from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email(self):
        '''Testing Creation Of new user with the help of Email'''
        email = 'test@test.com'
        password = 'Test@123'
        user = get_user_model().objects.create_user(
            email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        '''Testing The email for a new user is normalized'''
        email = 'test@TEST.COM'
        user = get_user_model().objects.create_user(
            email=email, password='test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_user(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                None, 'Test123')

    def test_create_new_super_user(self):
        '''Testing Creation of New Super User'''

        user = get_user_model().objects.create_superuser(
            'test@test.com', 'test@123')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
