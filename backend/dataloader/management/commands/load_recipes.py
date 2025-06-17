import json
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from recipes.models import Recipe, Tag, Ingredient, RecipeIngredient
from django.core.files import File

User = get_user_model()

class Command(BaseCommand):
    help = 'Load recipes from JSON file'

    def handle(self, *args, **options):
        file_path = r'C:\Users\Asus\Desktop\foodgram-st\data\recipes.json'
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'Файл {file_path} не найден!'))
            return
        with open(file_path, encoding='utf-8') as f:
            recipes = json.load(f)
        for data in recipes:
            author = User.objects.filter(username=data['author']).first()
            if not author:
                self.stdout.write(self.style.WARNING(f"Пользователь {data['author']} не найден, пропуск рецепта {data['name']}"))
                continue
            recipe = Recipe(
                name=data['name'],
                author=author,
                text=data['text'],
                cooking_time=data['cooking_time']
            )
            # Загрузка изображения, если есть
            image_path = os.path.join('C:\\Users\\Asus\\Desktop\\foodgram-st\\data', data.get('image', ''))
            if os.path.exists(image_path):
                with open(image_path, 'rb') as img_file:
                    recipe.image.save(os.path.basename(image_path), File(img_file), save=False)
            recipe.save()
            # Теги
            for tag_name in data.get('tags', []):
                tag = Tag.objects.filter(name=tag_name).first()
                if tag:
                    recipe.tags.add(tag)
            # Ингредиенты
            for ing in data.get('ingredients', []):
                ingredient = Ingredient.objects.filter(name=ing['name'], measurement_unit=ing['measurement_unit']).first()
                if ingredient:
                    RecipeIngredient.objects.create(
                        recipe=recipe,
                        ingredient=ingredient,
                        amount=ing['amount']
                    )
        self.stdout.write(self.style.SUCCESS('Successfully loaded recipes')) 