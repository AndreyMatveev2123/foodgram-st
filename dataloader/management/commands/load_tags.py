from django.core.management.base import BaseCommand
from recipes.models import Tag

class Command(BaseCommand):
    help = 'Load default tags'

    def handle(self, *args, **options):
        tags = [
            {'name': 'Завтрак', 'color': '#E26C2D', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#49B64E', 'slug': 'lunch'},
            {'name': 'Ужин', 'color': '#8775D2', 'slug': 'dinner'},
        ]
        
        for tag in tags:
            Tag.objects.get_or_create(
                name=tag['name'],
                color=tag['color'],
                slug=tag['slug']
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded tags')) 