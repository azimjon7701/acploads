from django.core.management import BaseCommand
from utils.distance import calc_distances_uncalced

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("command working...")
        calc_distances_uncalced()