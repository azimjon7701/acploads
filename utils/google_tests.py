import datetime

import googlemaps

gmaps = googlemaps.Client(key='AIzaSyD7Sbuc2E76Ht-VIQefQFUgtD253lVRkXk')


def partition(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i: i + size]


def distance_matrix(origins, destinations):
    t1 = datetime.datetime.now()
    result: dict = {}
    destinations_parts = list(partition(destinations, 20))
    result[origins]: dict = {}
    if origins and destinations:
        for destinations_part in destinations_parts:
            response = gmaps.distance_matrix(
                origins=origins,
                destinations=destinations_part
            )
            for i in range(len(response["destination_addresses"])):
                result[origins][destinations[i]] = response["rows"][0]["elements"][i]["distance"]["value"]
        t2 = datetime.datetime.now()
        return result
    return None


# o = 'Chikago, IL, USA'
# d = ['New York, Нью-Йорк, США', 'New Jersey Department of Health', 'Trenton, Нью-Джерси, США', 'Dallas, TX, USA',
#      'Los Angeles, CA, USA', 'Mexico City, CDMX, Mexico', 'Féniks، AZ, USA', 'Tucson, AZ, USA', 'Las Vegas, NV, USA',
#      'San Jose, CA, USA', 'Dallas, TX, USA', 'New Orleans, LA, USA', 'Mojave, CA, USA', 'Bakersfield, CA, USA',
#      'Dupree, SD, USA',
#      'Dayton, OH, USA', 'Sky Ranch, SD, USA', 'Onida, SD, USA', 'Melstone, MT, USA', 'Orleans, MA, USA',
#      'Lemmon, SD, USA',
#      'Hysham, MT, USA', 'Colstrip, MT, USA', 'Elgin, IL, USA', 'Randsburg, CA, USA', 'Rosamond, CA, USA',
#      'Santa Fe, NM, USA']
#
# print(distance_matrix(origins=o, destinations=d))
