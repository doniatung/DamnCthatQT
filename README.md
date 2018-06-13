## DamnCthatQT presents ...
# DateBrite!
Team Members: Donia Tung (Project Manager), Carol Pan, Taylor Wong, Queenie Xiang

SoftDev2 Pd 7

To Run, you should be able to simply [click here](http://datebrite.stuycs.org)

[Video!](https://youtu.be/xY3uT0df1oA)

proto0 is now [proto1](http://165.227.71.95/)

### Brief Overview: 
DateBrite is an app through which users can plan dates with their significant others, as well as functioning as a diary of sorts through which they can look through old dates. Upon creating an account, users will answer certain questions concerning how they enjoy spending their time, and we will use this data, along with the Eventbrite API to curate a homescreen with suggestions for potential date spots. Users are able to request information about a specific kind of event/action (like dinner, concert, etc), and the site will return a list of suggestions about where to find such activity. Once a user decides they would like to plan a given event for a date, they can select it to add onto their agenda. Once the date comes to pass, the user can upload pictures from that day or write a bit about how the date went.


### Running this project locally
#### Dependancies
  * flask
  * requests

`pip install -r requirements.txt`

if this fails, run `pip install <package name>` where package name is the individual package names listed above

#### Entering your virtual environment
First, make sure you have a virtual environment installed on your computer. If you don't, instructions for that can be [found here](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)

Then...

`. venv/bin/activate`
make sure you are in the `/datebrite/` directory of the repo and run

`python __init.py__`
