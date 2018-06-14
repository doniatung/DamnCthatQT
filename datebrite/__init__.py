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
current_user = ""

#App instantiation
app = Flask(__name__)
app.secret_key = os.urandom(32)


@app.route("/")
def welcome():
    if "username" in session:
        return render_template('index.html', logged = True)
    else:
        return render_template('index.html', logged = False)

@app.route("/login_redirect", methods=['GET'])
def login_redirect():
        #If logout:
        if "submit" in request.args and request.args["submit"] == "Logout":
		session.pop("username")
                session.pop("zipcode")
		flash("You logged out.")
                return redirect("/")

        #If logged in:
        if "username" in request.args and session.get('username'):
            return redirect("/")

        username = ""
        password = ""

        #Grabbing user info:
        args = request.args 
        if "username" in args and "password" in args:
		username = request.args["username"].lower()
		password = request.args["password"]

                print "\n DETECTED"
                print username
                print password

        #If not correct login info:
        if not database.auth(username, password):
                error = "Incorrect information. Please try again."
                return render_template("error.html", message=error)
        else:
              session["username"] = username
              session["zipcode"] = database.get_user(username)[6]
	      return redirect("/")


        return redirect("/")


@app.route('/browse')
def browse():
    if "username" in session:
        return render_template('browse.html', logged = True)
    else:
        return render_template('browse.html', logged = False)

@app.route('/about')
def about():
     if "username" in session:
        return render_template('about.html', logged = True)
     else:
        return render_template('about.html', logged = False)

@app.route('/view')
def view():
    return render_template('view.html')


@app.route('/account')
def account():
    if not "username" in session:
        return redirect("/login")
    else:
        user = session.get("username")
        data = database.get_user(user)
        print data
        firstname = data[1]
        lastname = data[2]
        email = data[3]
        zipcode = data[6]
        birthday = data[4]
        print user
        print firstname
        print lastname
        print email
        print zipcode
        print birthday
        
        return render_template("account.html", first=firstname, last=lastname, username=user, email=email, zipcode=zipcode, birthday=birthday) 
               
@app.route("/register", methods=['GET', 'POST'])
def create_acc():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/auth", methods=['GET'])
def auth_acc():
    args = request.args
    first = args["inputFirstName"]
    last = args["inputLastName"]
    bday = args["inputBDAY"]
    email = args["inputEmail"] 
    user = args["inputUsername"]
    pwd1 = args["inputPass1"]
    pwd2 = args["inputPass2"]
    zipcode = args["inputZip"]

    #print user
    #print pwd1
    #print pwd2
    #print zipcode
    
    success = database.create_acc(user, first, last, email, bday, pwd1, pwd2, zipcode)
    if (success):
        session["username"] = user
        return redirect("/")
    
    else:
        error="Unable to create your account at this time. Please try again."
        return render_template("error.html", message=error) 
     

@app.route("/friends")
def friends_list():
    user = session["username"]
    connections = database.check_connect(user)
    print connections
    users = database.get_users()
    #connections is a two part list
    print users
    
    return render_template("friends.html",lst = connections, users = users)

@app.route("/relationship")
def view_relationship():
    return render_templae("relationship.html")

@app.route("/other_user")
def view_user():
        user = request.args["user"]
        data = database.get_user(user)
        print data
        firstname = data[1]
        lastname = data[2]
        email = data[3]
        zipcode = data[6]
        birthday = data[4]
        print user
        print firstname
        print lastname
        print email
        print zipcode
        print birthday

        rel = database.get_relationship(session["username"], user)
        
        return render_template("account.html", first=firstname, last=lastname, username=user, email=email, zipcode=zipcode, birthday=birthday, rel = rel)

@app.route("/connect")
def connect():
    database.connect(session["username"], request.args["user"])
    return redirect("/view_user", user=request.args[user])

@app.route("/confirm")
def confirm():
    ship = request.args["shipid"]
    value = request.args["value"]
    database.respond(ship,value)
    return redirect("/friends")

@app.route("/yelp_search", methods=["GET"])
def yelp_search():
     if "username" in session:
        return render_template('yelp.html', logged = True)
     else:
        return render_template('yelp.html', logged = False)

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
            #print "GETTING HOME ZIP"
            #print session.get("username") 
            location = database.get_zipcode(session.get("username"))
            #print location
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
    

if __name__ == "__main__":
    #when we change to lamp stack, change debug to False
    app.debug = True
    app.run()
