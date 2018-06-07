import argparse
import json
import pprint
import requests
import sys
import urllib

API_KEY= 'l-2bZlJPHG6yODkqYMbtxTJBsz8uYwwRqOxNxAAF9N2NpHKGg20k7LN4xlrZWNFJ8HXhfhny4f6qgffSbSB9380jBKWWbLjt2mzEgmasp91BdcwxgEmBKW5gtDsQW3Yx'


API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


# Defaults 
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'New York, NY'
DEFAULT_SEARCH_LIMIT = 5
DEFAULT_SORT_BY = "best_match"
DEFAULT_PRICE = "1,2,3"


def search(term, location, search_limit, sort_by, price):

    message = ""
    
    if term == None:
        term = DEFAULT_TERM
        message = "No search category given, using default term of dinner" 

    if location == None:
        location = DEFAULT_LOCATION
        message = "No location given, using default location New York, NY"

    if search_limit == None:
        search_limit = DEFAULT_SEARCH_LIMIT
        message = "No search limit given, using default search limit 5" 

    if sort_by == None:
        sort_by = DEFAULT_SORT_BY
        message = "No sorting arrangement given, using default best match sorting"
    if price == None:
        price = DEFAULT_PRICE
        message = "No price range given, using default all price range"
    
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': search_limit,
        'sort_by': sort_by,
        'price': price
        
    }
    
    url = API_HOST+SEARCH_PATH
    print "URL Start:"
    print url

    
    headers = {
        'Authorization': 'Bearer %s' % API_KEY,
    }

    print "Headers:"
    print headers
    

    data = requests.request('GET', url, headers=headers, params=url_params)
    data = data.json()
    print "Data: \n"
    print data
    
    return data


def get_business(business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    data = requests.request(API_HOST, business_path, API_KEY)
    print "Data:"
    print data

    return data


def query_api(term, location):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    business_id = businesses[0]['id']

    print(u'{0} businesses found, querying business info ' \
        'for the top result "{1}" ...'.format(
            len(businesses), business_id))
    response = get_business(API_KEY, business_id)

    print(u'Result for business "{0}" found:'.format(business_id))
    
