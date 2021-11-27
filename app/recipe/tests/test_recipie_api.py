from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingrediant

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPIE_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_tag(user, name='Main Course'):
    return Tag.objects.create(user=user, name=name)


def sample_ingrediant(user, name='Cinnamon'):
    return Ingrediant.objects.create(user=user, name=name)


def sample_recipe(user, **params) -> Recipe:
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 5.00
    }

    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):
    '''Test unauthenticated recipie API access'''

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        '''Test that Authentication Required'''
        res = self.client.get(RECIPIE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'testpass'
        )

        self.client.force_authenticate(self.user)

    def test_retrive_recipe(self):
        '''Test retriving a list of recipies'''
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        recipes = Recipe.objects.all().order_by('-id')
        serialzer = RecipeSerializer(recipes, many=True)
        res = self.client.get(RECIPIE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialzer.data)

    def test_recipie_limited_to_user(self):
        '''Test Recipie Retriving For User'''

        user2 = get_user_model().objects.create_user(
            'test2@test.com',
            'testpass'
        )

        sample_recipe(user=self.user)
        sample_recipe(user=user2)

        res = self.client.get(RECIPIE_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serialzer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serialzer.data)

    def test_view_recipe_detail(self):
        '''Test viewing a recipe detail'''

        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingrediants.add(sample_ingrediant(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)
