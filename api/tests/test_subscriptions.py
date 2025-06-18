from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from users.models import Subscription

User = get_user_model()

class SubscriptionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        """Тест подписки на пользователя"""
        url = reverse('user-subscribe', args=[self.other_user.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Subscription.objects.filter(
                user=self.user,
                author=self.other_user
            ).exists()
        )

    def test_unsubscribe(self):
        """Тест отписки от пользователя"""
        Subscription.objects.create(user=self.user, author=self.other_user)
        url = reverse('user-subscribe', args=[self.other_user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Subscription.objects.filter(
                user=self.user,
                author=self.other_user
            ).exists()
        )

    def test_subscriptions_list(self):
        """Тест получения списка подписок"""
        Subscription.objects.create(user=self.user, author=self.other_user)
        url = reverse('user-subscriptions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_subscribe_to_self(self):
        """Тест попытки подписаться на самого себя"""
        url = reverse('user-subscribe', args=[self.user.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 