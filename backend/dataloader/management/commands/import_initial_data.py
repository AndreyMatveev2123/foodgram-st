import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Tag

class Command(BaseCommand):
    help = 'Imports initial data for Ingredients and Tags.'

    def handle(self, *args, **options):
        # Import Ingredients
        ingredients_file_path = os.path.join(settings.BASE_DIR.parent, 'data', 'ingredients.json')
        self.stdout.write(f'BASE_DIR: {settings.BASE_DIR}')
        self.stdout.write(f'Attempting to open: {ingredients_file_path}')
        self.stdout.write(f'Path exists: {os.path.exists(ingredients_file_path)}')
        try:
            with open(ingredients_file_path, 'r', encoding='utf-8') as f:
                ingredients_data = json.load(f)
                for item in ingredients_data:
                    Ingredient.objects.get_or_create(
                        name=item['name'],
                        measurement_unit=item['measurement_unit']
                    )
            self.stdout.write(self.style.SUCCESS('Successfully imported ingredients.'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'ingredients.json not found at {ingredients_file_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing ingredients: {e}'))

        # Create Tags
        tags = [
            {'name': 'Завтрак', 'color': '#E26C2D', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#427A59', 'slug': 'lunch'},
            {'name': 'Ужин', 'color': '#1E64F2', 'slug': 'dinner'},
            {'name': 'Десерт', 'color': '#8B4513', 'slug': 'dessert'},
        ]
        for tag_data in tags:
            Tag.objects.get_or_create(
                name=tag_data['name'],
                defaults={'color': tag_data['color'], 'slug': tag_data['slug']}
            )
        self.stdout.write(self.style.SUCCESS('Successfully created default tags.')) 