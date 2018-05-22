#zomato.py for accessing the Zomato API


import json
#import requests

#get the key
f = open('../.secret_key.txt', 'rU')
ZOMATO_KEY = json.loads(f.read())["zomato"] 
f.close()

print ZOMATO_KEY

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


