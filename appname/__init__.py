'''
DamnCThatQT
Donia Tung (PM), Carol Pan, Taylor Wong, Queenie Xiang
SoftDev2 pd7
P02 - Fin
'''

#initializing...
from flask import Flask, render_template, request
app = Flask("__name__")


@app.route("/")
def welcome():
    return "WIP - check us out later ;)"

if __name__ == "__main__":
    #when we change to lamp stack, change debug to False
    app.debug = True
    app.run()
