from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from recipes.models import Recipe, Tag, Ingredient, RecipeIngredient, ShoppingCart

User = get_user_model()

class ShoppingCartTests(TestCase):
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

    def test_add_to_shopping_cart(self):
        """Тест добавления рецепта в список покупок"""
        url = reverse('recipe-shopping-cart', args=[self.recipe.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            ShoppingCart.objects.filter(
                user=self.user,
                recipe=self.recipe
            ).exists()
        )

    def test_remove_from_shopping_cart(self):
        """Тест удаления рецепта из списка покупок"""
        ShoppingCart.objects.create(user=self.user, recipe=self.recipe)
        url = reverse('recipe-shopping-cart', args=[self.recipe.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            ShoppingCart.objects.filter(
                user=self.user,
                recipe=self.recipe
            ).exists()
        )

    def test_download_shopping_cart(self):
        """Тест скачивания списка покупок"""
        ShoppingCart.objects.create(user=self.user, recipe=self.recipe)
        url = reverse('recipe-download-shopping-cart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response['Content-Type'],
            'application/pdf'
        ) 