from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient

User = get_user_model()

class UserAuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123', first_name='Test', last_name='User'
        )
        self.client = APIClient()

    def test_user_registration(self):
        url = reverse('api:users-list')
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'newpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)

    def test_get_users_list(self):
        url = reverse('api:users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_get_me(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('api:users-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_auth_token(self):
        url = '/api/auth/token/login/'
        data = {'email': 'test@example.com', 'password': 'testpass123'}
        response = self.client.post(url, data)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_204_NO_CONTENT])

class TagIngredientTests(APITestCase):
    def setUp(self):
        Tag.objects.create(name='Завтрак', color='#E26C2D', slug='breakfast')
        Ingredient.objects.create(name='Соль', measurement_unit='г')

    def test_get_tags(self):
        url = reverse('api:tags-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_ingredients(self):
        url = reverse('api:ingredients-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_search_ingredient(self):
        url = reverse('api:ingredients-list') + '?search=Сол'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any('Соль' in i['name'] for i in response.data))

class RecipeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='author', email='author@example.com', password='authorpass', first_name='Author', last_name='Test'
        )
        self.other_user = User.objects.create_user(
            username='other', email='other@example.com', password='otherpass', first_name='Other', last_name='User'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.tag = Tag.objects.create(name='Обед', color='#00FF00', slug='lunch')
        self.ingredient = Ingredient.objects.create(name='Картофель', measurement_unit='кг')
        self.recipe_data = {
            'ingredients': [{'id': self.ingredient.id, 'amount': 2}],
            'tags': [self.tag.id],
            'image': '',  # Можно добавить base64-строку для картинки
            'name': 'Картофельное пюре',
            'text': 'Варить картофель, размять.',
            'cooking_time': 30
        }

    def test_create_recipe(self):
        url = reverse('api:recipes-list')
        data = self.recipe_data.copy()
        data['image'] = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 1)

    def test_get_recipe_list(self):
        Recipe.objects.create(
            name='Тестовый рецепт', text='Описание', cooking_time=10, author=self.user
        )
        url = reverse('api:recipes-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_update_recipe(self):
        recipe = Recipe.objects.create(
            name='Старое имя', text='Описание', cooking_time=10, author=self.user
        )
        url = reverse('api:recipes-detail', args=[recipe.id])
        data = {'name': 'Новое имя', 'text': 'Описание', 'cooking_time': 15}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.name, 'Новое имя')

    def test_delete_recipe(self):
        recipe = Recipe.objects.create(
            name='Удаляемый', text='Описание', cooking_time=10, author=self.user
        )
        url = reverse('api:recipes-detail', args=[recipe.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_add_remove_favorite(self):
        recipe = Recipe.objects.create(
            name='Любимый', text='Описание', cooking_time=10, author=self.user
        )
        url = reverse('api:recipes-favorite', args=[recipe.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_add_remove_shopping_cart(self):
        recipe = Recipe.objects.create(
            name='В корзину', text='Описание', cooking_time=10, author=self.user
        )
        url = reverse('api:recipes-shopping-cart', args=[recipe.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_download_shopping_cart(self):
        recipe = Recipe.objects.create(
            name='В корзину', text='Описание', cooking_time=10, author=self.user
        )
        RecipeIngredient.objects.create(recipe=recipe, ingredient=self.ingredient, amount=2)
        url = reverse('api:recipes-shopping-cart', args=[recipe.id])
        self.client.post(url)
        url = reverse('api:recipes-download-shopping-cart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Список покупок', response.content.decode())

class SubscribeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='main', email='main@example.com', password='mainpass', first_name='Main', last_name='User'
        )
        self.author = User.objects.create_user(
            username='author', email='author@example.com', password='authorpass', first_name='Author', last_name='Test'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_subscribe_unsubscribe(self):
        url = reverse('api:users-subscribe', args=[self.author.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_subscriptions_list(self):
        url = reverse('api:users-subscribe', args=[self.author.id])
        self.client.post(url)
        url = reverse('api:users-subscriptions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

# Аналогично добавим тесты для Favorite, ShoppingCart, Subscribe и download_shopping_cart
# (их добавлю после подтверждения структуры и подхода) 