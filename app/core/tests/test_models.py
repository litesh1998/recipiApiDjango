from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

from unittest.mock import patch


def sample_user(email='test@test.com', password='test123'):
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        '''Test the tag string representation'''
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingrediant_str(self):
        '''Test the string representation of ingredients'''

        ingredient = models.Ingrediant.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        '''Test the string representation of a string'''
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and Mushroom Sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
