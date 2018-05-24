import urllib2
import requests
import json
import os

f = open('./.secret_key.txt', 'rU')
keys = json.loads(f.read())
f.close()

ZOMATO_KEY = keys['zomato']
#FOOD_KEY = keys['food2fork_key']
ZOMATO_URL = 'https://developers.zomato.com/api/v2.1/'

ZOMATO_HEADER = {'user-key': ZOMATO_KEY}


def restaurant_search(query, location, radius, max_amt,
                        cuisines, sort, order):
    '''Return the restaurants that match the parameters given.'''
    url = ZOMATO_URL + "search"

    if location != '':
        location = find_location(query=location)[0]
    else:
        location = {'latitude': None, 'longitude': None}

    params = {
                'q': query,
                'lat': location['latitude'],
                'lon': location['longitude'],
                'radius': radius,
                'count': max_amt,
                'cuisines': cuisines,
                'sort': sort,
                'order': order
            }
    try:
        req = requests.get(url, headers=ZOMATO_HEADER, params=params)
        # print req.url
        restaurants = req.json()
    except HTTPError:
        return None
    return restaurants


def restaurant_info(res_id):
    '''Return the Zomato API information about a specific restaurant.'''
    url = ZOMATO_URL + 'restaurant'
    params = {'res_id': res_id}
    req = requests.get(url, headers=ZOMATO_HEADER, params=params)
    info = req.json()
    return info

def find_location(query, max_amt=1):
    '''Return the Zomato API information about a location.'''
    url = ZOMATO_URL + "locations"
    if max_amt < 1:
        return []
    params = {'query': query,
              'count': max_amt}
    req = requests.get(url, headers=ZOMATO_HEADER, params=params)
    locs = req.json()
    return locs['location_suggestions']

