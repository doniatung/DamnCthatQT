#maps.py for accessing Google Maps API
import json

#get the key
f = open('../.secret_key.txt', 'rU')
MAP_KEY = json.loads(f.read())["googlemaps"]
f.close()
