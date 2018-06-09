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
from utils import database

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
def create_acc(): #needs zip and redirect towards /auth
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/auth")
def auth_acc():
    '''PSEUDO CODE
    if (here_to_signup):
        success = database.create_acc(user, pwd1, pwd2, zipcode)
        if (success):
            return redirect to home?
        else:
            return to signup page with prompt: "account creation unsuccessful"
     else: #here to login
        success = database.auth(user, pwd)
        if (success):
            return redirect to account page
        else:
            return error prompt on login page
     '''

    return "WIP - check us out later ;)"

@app.route("/friends")
def friends_list():
    '''PSUEDO CODE:
    connections = database.check_connect(user)

    #connections is a two part list
    '''
    
    return render_template("friends.html") #,lst = connections)

@app.route("/relationship")
def view_relationship():
    return render_templae("relationship.html")

@app.route("/user")
def view_user():
    '''PSEUDO CODE:
    relationship = database.get_relationship(user1,user2)
    '''
    return "idk"

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
    sort_by = args["sort"]
    price = args["price"]
    if "home" in args: 
        use_home_address = args["home"]
        if use_home_address == "true":
            location = '''RETRIEVE HOME ADDRESS'''

    data = yelp.search(term, location, search_limit, sort_by, price)

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
    app.debug = True
    app.run()
