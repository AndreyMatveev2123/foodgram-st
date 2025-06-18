import csv
import os
from django.core.management.base import BaseCommand
from recipes.models import Tag
from django.conf import settings


class Command(BaseCommand):
    help = "Импорт тегов из CSV файла в базу данных"

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, "data", "tags.csv")
        file_path = os.path.normpath(file_path)
        count = 0
        with open(file_path, encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 3:
                    name, color, slug = row
                    obj, created = Tag.objects.get_or_create(
                        name=name.strip(),
                        color=color.strip(),
                        slug=slug.strip()
                    )
                    if created:
                        count += 1
        self.stdout.write(
            self.style.SUCCESS(f"Импортировано {count} новых тегов")
        ) 