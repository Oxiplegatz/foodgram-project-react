import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        path = f'{settings.BASE_DIR}/data/ingredients.csv'
        with open(path, 'rt') as csv_file:
            reader = csv.reader(csv_file, dialect='excel')
            for row in reader:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1],
                )
