from django.core.management import BaseCommand
from utils.load_excel import load_excel
from places.models import Place
from utils.es_connection import connection
from utils.elasticsearch_func import recreate_index
class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Filling places...")
        places = load_excel()
        for place in places:
            try:
                place_obj = Place.objects.get_or_create(
                    name=place[0],
                    latitude=place[1],
                    longitude=place[2]
                )
            except Exception as e:
                print("Error:",e)
        # recreate_index(connection())
