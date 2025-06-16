import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from recipes.models import Recipe, Ingredient, Tag, RecipeIngredient

User = get_user_model()


class Command(BaseCommand):
    help = "Creates test users and recipes."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Creating test users and recipes..."))

        # Create Users
        users_to_create = [
            {
                "email": "testuser1@example.com",
                "username": "testuser1",
                "first_name": "Тест",
                "last_name": "Пользователь1",
                "password": "testpass123",
            },
            {
                "email": "testuser2@example.com",
                "username": "testuser2",
                "first_name": "Тест",
                "last_name": "Пользователь2",
                "password": "testpass123",
            },
        ]

        created_users = []
        for user_data in users_to_create:
            user, created = User.objects.get_or_create(
                email=user_data["email"],
                defaults={
                    "username": user_data["username"],
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"],
                },
            )
            if created:
                user.set_password(user_data["password"])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user: {user.username}"))
            else:
                self.stdout.write(
                    self.style.WARNING(f"User already exists: {user.username}")
                )
            created_users.append(user)

        # Create Recipes
        if not created_users:
            self.stdout.write(
                self.style.ERROR(
                    "No users to create recipes for. Please create users first."
                )
            )
            return

        ingredients = list(
            Ingredient.objects.all()[:5]
        )  # Get some existing ingredients
        tags = list(Tag.objects.all()[:3])  # Get some existing tags

        if not ingredients:
            self.stdout.write(
                self.style.ERROR(
                    "No ingredients found. Please import ingredients first."
                )
            )
            return
        if not tags:
            self.stdout.write(
                self.style.ERROR("No tags found. Please create tags first.")
            )
            return

        for i, user in enumerate(created_users):
            recipe_name = f"Тестовый рецепт {i+1} от {user.username}"
            recipe_text = (
                f"Это тестовый рецепт, созданный пользователем {user.username}."
            )

            # Using a minimal base64 image for testing
            test_image_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

            recipe, created = Recipe.objects.get_or_create(
                name=recipe_name,
                defaults={
                    "author": user,
                    "image": test_image_base64,  # This will be handled by Base64ImageField
                    "text": recipe_text,
                    "cooking_time": (i + 1) * 10,  # Example cooking time
                },
            )

            if created:
                # Add tags
                recipe.tags.set(tags)

                # Add ingredients with amounts
                for ing_idx, ingredient in enumerate(ingredients):
                    RecipeIngredient.objects.get_or_create(
                        recipe=recipe,
                        ingredient=ingredient,
                        defaults={"amount": (ing_idx + 1) * 10},
                    )
                self.stdout.write(self.style.SUCCESS(f"Created recipe: {recipe.name}"))
            else:
                self.stdout.write(
                    self.style.WARNING(f"Recipe already exists: {recipe.name}")
                )

        self.stdout.write(self.style.SUCCESS("Test data creation finished."))
