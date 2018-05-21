#event.py for accessing the EventBrite API
import json

#get the key
f = open('../.secret_key.txt', 'rU')
EVENTBRITE_KEY = json.loads(f.read())["eventbrite"]
f.close()
