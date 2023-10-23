import csv

from django.core.management.base import BaseCommand

from recipies.models import Ingredient
from backend.constants import CSV_PATH


class Command(BaseCommand):
    help = "Заполнение БД ингредиентами"

    def handle(self, *args, **kwargs):
        with open(CSV_PATH, encoding='utf-8') as file:
            csvreader = csv.reader(file)
            next(csvreader)
            for row in csvreader:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1],
                )
