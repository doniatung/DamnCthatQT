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
import zomato

#App instantiation
app = Flask(__name__)
app.secret_key = os.urandom(32)


@app.route("/")
def welcome():
    return render_template('index.html')

@app.route('/browse')
def browse():
    return render_template('browse.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route("/register")
def create_acc():
    return "WIP - check us out later ;)"

@app.route("/login")
def login():
    return "WIP - check us out later ;)"

@app.route("/auth")
def auth_acc():
    return "WIP - check us out later ;)"

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
