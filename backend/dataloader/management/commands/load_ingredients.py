import csv
from django.core.management.base import BaseCommand
from recipes.models import Ingredient

class Command(BaseCommand):
    help = 'Load ingredients from CSV file'

    def handle(self, *args, **options):
        file_path = r'C:\Users\Asus\Desktop\foodgram-st\data\ingredients.csv'
        print(f'Ищу файл по пути: {file_path}')
        with open(file_path, encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                name, measurement_unit = row
                Ingredient.objects.get_or_create(
                    name=name,
                    measurement_unit=measurement_unit
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded ingredients')) 