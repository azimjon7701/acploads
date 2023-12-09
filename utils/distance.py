import datetime
import googlemaps
from main.models import Distance,Load,Search
from utils.helpers import get_time_limit_hour_query

gmaps = googlemaps.Client(key='AIzaSyD7Sbuc2E76Ht-VIQefQFUgtD253lVRkXk')


def partition(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i: i + size]

def calc_distance(search_id,query):
    search = Search.objects.get(id=search_id)
    old_addresses = [a.load_address for a in Distance.objects.filter(search_address=search.origin)]
    loads = Load.objects.filter(query & get_time_limit_hour_query()).exclude(origin__in=old_addresses).exclude(origin='')
    origins = list(set([l.origin for l in loads]))
    distance_matrix(search.origin, origins)
    old_addresses = [a.load_address for a in Distance.objects.filter(search_address=search.destination)]
    loads = Load.objects.filter(get_time_limit_hour_query()).exclude(destination__in=old_addresses).exclude(destination='')
    destinations = list(set([l.destination for l in loads]))
    distance_matrix(search.destination, destinations)

def calc_distances_uncalced():
    searches = Search.objects.all()
    for search in searches:
        origins = []
        old_addresses = [a.load_address for a in Distance.objects.filter(search_address=search.origin)]
        loads = Load.objects.all().exclude(origin__in=old_addresses).exclude(origin='')
        origins = list(set([l.origin for l in loads]))
        distance_matrix(search.origin, origins)
        destinations = []
        old_addresses = [a.load_address for a in Distance.objects.filter(search_address=search.destination)]
        loads = Load.objects.all().exclude(destination__in=old_addresses).exclude(destination='')
        destinations = list(set([l.destination for l in loads]))
        distance_matrix(search.destination, destinations)
        print("found uncalced:",len(origins),len(destinations))


def distance_matrix(origins, destinations):
    distances = Distance.objects.filter(search_address=origins)
    result: dict = {}
    destinations_parts = list(partition(destinations, 20))
    result[origins]: dict = {}
    if origins and destinations:
        for destinations_part in destinations_parts:
            response = gmaps.distance_matrix(
                origins=origins,
                destinations=destinations_part
            )
            for i in range(len(destinations_part)):
                if response["rows"][0]["elements"][i].get("distance",None):
                    if len(distances.filter(load_address=destinations_part[i])) == 0:
                        try:
                            distance = float(response["rows"][0]["elements"][i]["distance"]["value"])*0.00062137
                        except:
                            distance = 'none'
                        if distance != 'none':
                            Distance.objects.create(
                                search_address=origins,
                                load_address=destinations_part[i],
                                distance=float(response["rows"][0]["elements"][i]["distance"]["value"])*0.00062137
                            )

    return None

def get_radius(search_id, load_id,point):
    r = '-'
    try:
        search = Search.objects.get(id=search_id)
        load = Load.objects.get(id=load_id)
        if point == 'o':
            if load.origin and search.origin:
                distance_o = Distance.objects.filter(search_address=search.origin).filter(load_address=load.origin)
                d_o = distance_o[0].distance if distance_o else 'none'
                if d_o != 'none':
                    r = round(d_o)
        elif point == 'd':
            if load.destination and search.destination:
                distance_o = Distance.objects.filter(search_address=search.origin).filter(load_address=load.origin)
                distance_d = Distance.objects.filter(search_address=search.destination).filter(load_address=load.destination)
                d_d = distance_d[0].distance if distance_d else 'none'
                if d_d != 'none':
                    r = round(d_d)
    except:
        r = '-'
    return r


