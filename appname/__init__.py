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
    return "WIP - check us out later ;)"

@app.route("/signup")
def create_acc():
    return "WIP - check us out later ;)"

@app.route("/login")
def login():
    return "WIP - check us out later ;)"

@app.rout("/auth")
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


if __name__ == "__main__":
    #when we change to lamp stack, change debug to False
    app.debug = True
    app.run()
