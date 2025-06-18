from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from recipes.models import Recipe, Tag, Ingredient, RecipeIngredient

User = get_user_model()

class RecipeTests(TestCase):
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

    def test_create_recipe(self):
        """Тест создания рецепта"""
        url = reverse('recipe-list')
        data = {
            'name': 'Новый рецепт',
            'text': 'Описание нового рецепта',
            'cooking_time': 45,
            'tags': [self.tag.id],
            'ingredients': [
                {
                    'id': self.ingredient.id,
                    'amount': 3
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 2)

    def test_get_recipe_list(self):
        """Тест получения списка рецептов"""
        url = reverse('recipe-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_recipe_detail(self):
        """Тест получения детальной информации о рецепте"""
        url = reverse('recipe-detail', args=[self.recipe.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Тестовый рецепт')

    def test_update_recipe(self):
        """Тест обновления рецепта"""
        url = reverse('recipe-detail', args=[self.recipe.id])
        data = {
            'name': 'Обновленный рецепт',
            'text': 'Обновленное описание',
            'cooking_time': 60,
            'tags': [self.tag.id],
            'ingredients': [
                {
                    'id': self.ingredient.id,
                    'amount': 4
                }
            ]
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.name, 'Обновленный рецепт')

    def test_delete_recipe(self):
        """Тест удаления рецепта"""
        url = reverse('recipe-detail', args=[self.recipe.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.count(), 0) 