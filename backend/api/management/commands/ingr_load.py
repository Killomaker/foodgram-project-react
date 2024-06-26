import csv

from django.core.management.base import BaseCommand

from backend.settings import LOAD_DATABASE
from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        with open(
            f'{LOAD_DATABASE}/ingredients.csv', encoding='utf-8'
        ) as file:
            reader = csv.reader(file)
            next(reader)
            ingredients = [
                Ingredient(
                    name=row[0],
                    measurement_unit=row[1],
                )
                for row in reader
            ]
            Ingredient.objects.bulk_create(ingredients)
