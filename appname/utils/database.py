#DamnCThatQT
#Donia Tung (PM), Carol Pan, Taylor Wong, Queenie Xiang
#SoftDev2 pd7
#P02 - Fin



''' List of methods
setup() - sets up db

create_acc(user,pwd1,pwd2,zip) - sees if input is valid, adds acc to db
    returns (T/F, T/F) -- (is username valid, is password valid)

auth(user,pwd) - checks if user and pwd match
    returns T/F

add_interest(user,like) - adds user interest individually
    returns T/F

get_interest(user) - procures a tuple of all user interests
    returns (T/F, tuple) -- (did it work, interests)

get_users() - gets all users
    returns (T/F, list of users)

connect(origUser, otherUser) - adds the pairing of user1 and user2 into the db
    returns T/F

check_connect(user) - gets all the dates that user is planning from dates table
    returns ((ppl user likes),(ppl who likes user))

respond(shipid, val) - invited user agrees to date (val = 1) or rejects (val = -1)
    returns T/F

get_relationship(user1, user2) - check the relationship between two users (if there is one)
    returns [(sqlite_entry), (planned_dates)
            (shipid, user1, user2, status (-1=off,1=on,0=tbd), pts)
            (dateid, shipid, date, status)

#note: the following is not done
start_date(shipid) - starts a date for this pair
    returns T/F

complete_date(dateid) - ends date for this pair
    returns T/F

add_event(dateid, event, location, time) - adds event to date
    returns T/F

get_plan(dateid) - gets all the events listed in the date

add_image(dateid, imgfile, location) - adds image to db under appropriate event
    returns T/F
'''

global db
import sqlite3
import hashlib
import time

#open database
def open_db():
    global db
    f = "../data/dating.db" #CHANGE BACK
    db = sqlite3.connect(f, check_same_thread = False)
    return db.cursor()

#close database
def close_db():
    global db
    db.commit()
    db.close()
    return

#SETUP - TO BE RUN EACH TIME
#------------------------------------
def setup():
    c= open_db()
    
    #acc table
    stmt= "CREATE TABLE IF NOT EXISTS accounts(user TEXT PRIMARY KEY, pass TEXT, zip TEXT)"
    c.execute(stmt)
    #user likes (are dislikes necessary?)
    stmt= "CREATE TABLE IF NOT EXISTS likes(user TEXT, like TEXT, PRIMARY KEY(user,like))"
    c.execute(stmt)
    #pairing up
    stmt = "CREATE TABLE IF NOT EXISTS ships(shipid INT PRIMARY KEY, user1 TEXT, user2 TEXT, status INT, points INT)"
    c.execute(stmt)
    #dates
    stmt= "CREATE TABLE IF NOT EXISTS dates(dateid INT PRIMARY KEY, shipid INT, date TEXT, status INT)"
    c.execute(stmt)
    #planning
    stmt = "CREATE TABLE IF NOT EXISTS planner(dateid INT, event TEXT, location TEXT,time TEXT)"
    c.execute(stmt)
    #images
    stmt= "CREATE TABLE IF NOT EXISTS imgs(dateid INT, place TEXT, address TEXT, image BLOB)"
    c.execute(stmt)

    close_db()
    return
#=====================================


#CREATE AN ACCOUNT
#-------------------------------------
def create_acc(user, pwd1, pwd2, zipcode):
    global db
    try:
        user=user.strip().lower()
        c = open_db()
        #hashing pwd
        obj = hashlib.sha224(pwd1)
        hash_pwd = obj.hexdigest()

        command = "INSERT INTO accounts VALUES(?,?,?)"
        c.execute(command, (user,hash_pwd,zipcode)) #try to see if user exists
        #if pwds don't match
        if pwd1 != pwd2:
            print "passwords don't match"
            db.close() #don't commit and close
            return (True, False)
        else:
            close_db() #commit and close
            return (True, True)

    except: #if user exists, code will jump here
        print "Error: account cannot be created"
        return (False, False)

#=======================================


#AUTHENTICATE USER
#---------------------------------------
#returns true or false
#previously (has passwords?, correct password?)
def auth(user, pwd):
    global db
    try:
        user=user.strip().lower()
        c = open_db()
        command = "SELECT pass FROM accounts WHERE user=?"
        c.execute(command, (user,))
        pwds = c.fetchall()
        close_db()
    except:
        print "Error: authenticate call not made"
        return False #(False, False)
    if len(pwds) == 0:
        return False #(False, False)
    #hashing pwd
    obj = hashlib.sha224(pwd)
    hash_pwd = obj.hexdigest()
    if pwds[0][0] == hash_pwd:
        return True #(True, True)
    else:
        return False #(False, True)
#========================================


#ADD INTEREST
#----------------------------------------
def add_interest(user, like):
    global db
    try:
        user=user.strip().lower()
        like = like.strip().lower()
        c = open_db()
        
        command = "INSERT INTO likes VALUES(?,?)"
        c.execute(command, (user,like)) #insert
        close_db()
    except:
        print "Error: like " + like + " already registered"
        return False
    
    return True
#========================================

#GET INTEREST (FOR EVENTBRITE)
#----------------------------------------
def get_interest(user):
    global db
    try:
        user = user.strip().lower()
        c = open_db()

        command = "SELECT like FROM likes WHERE user=?"
        likes = c.execute(command, (user,))
        close_db()
    except:
        print "Error: could not make call on interest"
        return (False,)
    return (True, likes)
#=========================================  


#GET USERS
#-----------------------------------------
def get_users():
    global db
    try:
        c = open_db()

        command = "SELECT user FROM accounts"
        users = c.execute(command)
        close_db()
    except:
        print "Error: could not get list of users"
        return (False,)
    return (True, users)
#==========================================


#CONNECT USERS (USER1 initiates connection)
#------------------------------------------
def connect(user1,user2):
    global db
    try:
        c = open_db()

        command = "INSERT INTO ships VALUES(?,?,0)"
        c.execute(command, (user1,user2))
        close_db()
    except:
        print "Error: could not connect users"
        return False
    return True
#===========================================


#CHECK CONNECTIONS (WHO USER IS CONNECTED TO)
#-------------------------------------------
def check_connect(user):
    global db
    try:
        c = open_db()

        command = "SELECT * FROM ships WHERE user1 = ? AND status != -1"
        lst1 = list(c.execute(command, (user1,)))
        command = "SELECT * FROM ships WHERE user2 = ? AND status = 1"
        lst2 = list(c.execute(command, (user1,)))
        command = "SELECT * FROM ships WHERE user2 = ? AND status = 0"
        lst3 = list(c.execute(command, (user1,)))
        close_db()
    except:
        print "Error: could not pull connections"
        return []
    return [lst1.extend(lst2), lst3]
#===========================================


#USER2 RESPONDS
#-------------------------------------------
def respond(shipid, val):
    global db
    try:
        c = open_db()

        command = "UPDATE ships SET status = ? WHERE shipid = ?"
        c.execute(command, (val, shipid))
        close_db()

    except:
        print "Error: could not update relationship"
        return False
    return True
#============================================


#FIND RELATIONSHIP BETWEEN TWO USERS
#--------------------------------------------
def get_relationship(user1,user2):
    global db
    try:
        c = open_db()

        command = "SELECT * FROM ships WHERE user1 = ? AND status != -1"
        lst1 = list(c.execute(command, (user1,)))
        command = "SELECT * FROM ships WHERE user2 = ? AND status = 1"
        lst2 = list(c.execute(command, (user1,)))
    except:
        print "Error: could not get details"
        return []
    return lst1 + lst2
#==============================================

def add_event(dateid, event, location, time):
    global db
    return
#setup()


'''testing'''
#print create_acc("crashley", "bubba", "bubba", 10000)
#print auth("crashley", "bobba")
'''
likes = ["happiness", "butter", "butterflies", "good mac and cheese", "sing", "song", "sing"]
for entry in likes:
    add_interest("crashley", entry)
'''
