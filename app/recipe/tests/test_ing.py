from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingrediant

from recipe.serializers import IngrediantSerializer

INGREDIANT_URL = reverse('recipe:ingrediant-list')


class PublicIngrediantApiTests(TestCase):
    '''Test the publically available ingrediants API'''

    def setUp(self):
        self.client = APIClient()

    def test_login_requireed(self):
        '''Test that login is required to access the endpoint'''
        res = self.client.get(INGREDIANT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngrediantApiTests(TestCase):
    '''Test the authorised user ingrediants API'''

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'test123'
        )
        self.client.force_authenticate(self.user)

    def test_retrive_ingrediant_list(self):
        '''Test Retriving a list of ingrediants'''

        Ingrediant.objects.create(user=self.user, name='Kale')
        Ingrediant.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDIANT_URL)

        ingrediants = Ingrediant.objects.all().order_by('-name')
        serializer = IngrediantSerializer(ingrediants, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingrediants_limited_to_user(self):

        user2 = get_user_model().objects.create_user(
            'test2@test.com',
            'test123'
        )

        Ingrediant.objects.create(user=user2, name='Vinegar')
        ingrediant = Ingrediant.objects.create(user=self.user, name='Termaric')

        res = self.client.get(INGREDIANT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingrediant.name)

    def test_create_ingrediant_successful(self):
        payload = {'name': 'Cabbage'}
        self.client.post(INGREDIANT_URL, payload)

        exits = Ingrediant.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exits)

    def test_create_tag_invalid(self):
        '''Test creating a new tag with invalid payload'''
        payload = {'name': ''}
        res = self.client.post(INGREDIANT_URL, payload)

        self.assertTrue(res.status_code, status.HTTP_400_BAD_REQUEST)
