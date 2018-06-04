#event.py for accessing the EventBrite API
import json

#get the key
f = open('../.secret_key.txt', 'rU')
EVENTBRITE_KEY = json.loads(f.read())["eventbrite"]
f.close()


def get_events(like, zipcode):
    url = "https://www.eventbriteapi.com/v3/events/search/?token=" \
          + EVENTBRITE_KEY + "&q=" + like + "&location.address=" + zipcode\
          + "&location.within=50mi"
    response = urllib2.urlopen(url)
    url = response.geturl()
    info = response.read()
    info = json.loads(info)
    #print info
    return info

