from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from recipes.models import Recipe, Tag, Ingredient, RecipeIngredient, Favorite

User = get_user_model()

class FavoriteTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        # Создаем теговые данные
        self.tag = Tag.objects.create(
            name='Завтрак',
            color='#E26C2D',
            slug='breakfast'
        )
        
        # Создаем ингредиенты
        self.ingredient = Ingredient.objects.create(
            name='Яйцо',
            measurement_unit='шт'
        )
        
        # Создаем тестовый рецепт
        self.recipe = Recipe.objects.create(
            author=self.user,
            name='Тестовый рецепт',
            text='Описание тестового рецепта',
            cooking_time=30
        )
        self.recipe.tags.add(self.tag)
        RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            amount=2
        )

    def test_add_to_favorites(self):
        """Тест добавления рецепта в избранное"""
        url = reverse('recipe-favorite', args=[self.recipe.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Favorite.objects.filter(
                user=self.user,
                recipe=self.recipe
            ).exists()
        )

    def test_remove_from_favorites(self):
        """Тест удаления рецепта из избранного"""
        Favorite.objects.create(user=self.user, recipe=self.recipe)
        url = reverse('recipe-favorite', args=[self.recipe.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Favorite.objects.filter(
                user=self.user,
                recipe=self.recipe
            ).exists()
        )

    def test_favorites_list(self):
        """Тест получения списка избранных рецептов"""
        Favorite.objects.create(user=self.user, recipe=self.recipe)
        url = reverse('recipe-list')
        response = self.client.get(url, {'is_favorited': '1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 