'''
DamnCThatQT
Donia Tung (PM), Carol Pan, Taylor Wong, Queenie Xiang
SoftDev2 pd7
P02 - Fin
'''

from flask import Flask, session, url_for, redirect, render_template, request, flash
import urllib2
import requests
import json
import os
from utils import zomato
from utils import yelp

#from jinja2 import jinja2.ext.do

d = {} 

#App instantiation
app = Flask(__name__)
app.secret_key = os.urandom(32)


@app.route("/")
def welcome():
    return render_template('index.html')

@app.route("/login_redirect")
def login_redirect():
        #If logout:
        if "submit" in request.args and request.args["submit"] == "Logout":
		session["username"] = ""
		flash("You logged out.")
                return redirect("/")

        #If logged in:
        if "username" in request.args and session.get('username'):
                return redirect("/")

        username = ""
        password = ""

        #Grabbing user info:
        if "user" in request.args and "pass" in request.args:
		username = request.args["user"].lower()
		password = request.args["pass"]

        #If not correct login info:
        '''
        if not database.verify_user(username, password):
                error = "Incorrect information. Please try again."
                return render_template("error.html", error=error)
        else:
              session["username"] = username
	      return redirect("/")

        '''
        return redirect("/")


@app.route('/browse')
def browse():
    return render_template('browse.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/view')
def view():
    return render_template('view.html')


@app.route('/account')
def account():
    return render_template('account.html')

@app.route("/register")
def create_acc():
    return render_template("signup.html")

@app.route("/login")
def login():
    return "WIP - check us out later ;)"

@app.route("/auth")
def auth_acc():
    return "WIP - check us out later ;)"


@app.route("/yelp_search", methods=["GET"])
def yelp_search():
    return render_template("yelp.html")

@app.route("/yelp_results", methods=["GET"])
def yelp_results():
    global d 
    args = request.args
    term = args["term"]
    location = args["location"]
    search_limit = args["search_limit"]

    data = yelp.search(term, location, search_limit)

    #print data 
    #print data["businesses"]
    #print "\n TESTING \n"

    businesses = data["businesses"]

    #print "\ntest:"
    #print d
    #print "\n"
    #print "name" 
    #print d["name"]
        
    return render_template("yelp_results.html", data = businesses, search_limit=search_limit) 
    
#ZOMATO STUFF#
@app.route("/restaurant_search", methods=["GET"])
def rest_search():
    return render_template("zomato.html")

@app.route("/restaurant_results", methods=["GET"])
def restaurant_results():
    args = request.args

    if args['cuisines']:
        cuisines = args['cuisines'].split(',')
    else:
        cuisines = []

    try:
        sort = args['sort']
    except KeyError:
        sort = 'rating'
    try:
        order = args['order']
    except KeyError:
        order = 'desc'

    '''
    if args['query'] or args['max_amt'] or len(cuisines) == 0:
        print args['query']
        print args['max_amt']
        print len(cuisines)

        return render_template("error.html", message="Incorrect inputs or missing inputs, please try again")

    '''

    data = zomato.restaurant_search(args['query'],
                    args['location'],
                    args['radius'],
                    args['max_amt'],
                    cuisines,
                    sort,
                    order)

    print data

    return render_template("zomato_results.html",
                           rests = data['restaurants'],
                           num = data['results_shown'])


if __name__ == "__main__":
    #when we change to lamp stack, change debug to False
    app.debug = False
    app.run()
