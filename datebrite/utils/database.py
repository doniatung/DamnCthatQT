#DamnCThatQT
#Donia Tung (PM), Carol Pan, Taylor Wong, Queenie Xiang
#SoftDev2 pd7
#P02 - Fin



''' List of methods [x] marks issues
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

get_zipcode() - gets zipcode of a certain user 
    returns zipcode (int) 

connect(origUser, otherUser) - adds the pairing of user1 and user2 into the db
    returns T/F
    BUT: user2 has to agree to be official
    
check_connect(user) - gets all the dates that user is planning from dates table
    returns {"confirmed": lst of ships, "pending": lst of ships}
    (id, user1, user2, status(whether user2 agrees), pts)

respond(shipid, val) - invited user agrees to date (val = 1) or rejects (val = -1)
    returns T/F

get_relationship(user1, user2) - check the relationship between two users (if there is one)
    returns [(sqlite_entry), (planned_dates)]
            (shipid, user1, user2, status (-1=off,1=on,0=tbd), pts)
            (dateid, shipid, date, status)

start_date(shipid, text) - starts a date for this pair
    returns T/F

complete_date(dateid) - ends date for this pair
    returns T/F

add_event(dateid, event, location, time) - adds event to date
    returns T/F

get_plan(dateid) - gets all the events listed in the date


#below not tested
add_image(dateid, imgfile, place, address) - adds image to db under appropriate event
    returns T/F

get_imgs(dateid)
'''

global db
import sqlite3
import hashlib
import time

#open database
def open_db():
    global db
    f = "data/dating.db" #CHANGE BACK
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
    stmt= "CREATE TABLE IF NOT EXISTS accounts(user TEXT PRIMARY KEY, firstname TEXT, lastname TEXT, email BLOB, birthday BLOB, pass TEXT, zip TEXT)"
    c.execute(stmt)
    #user likes (are dislikes necessary?)
    stmt= "CREATE TABLE IF NOT EXISTS likes(user TEXT, like TEXT, PRIMARY KEY(user,like))"
    c.execute(stmt)
    #pairing up
    stmt = "CREATE TABLE IF NOT EXISTS ships(shipid INTEGER PRIMARY KEY, user1 TEXT, user2 TEXT, status INTEGER, pts INTEGER)"
    c.execute(stmt)
    #dates
    stmt= "CREATE TABLE IF NOT EXISTS dates(dateid INTEGER PRIMARY KEY, date TEXT, shipid INTEGER, status INTEGER)"
    c.execute(stmt)
    #planning
    stmt = "CREATE TABLE IF NOT EXISTS planner(dateid INTEGER, event TEXT, location TEXT, time TEXT)"
    c.execute(stmt)
    #images
    stmt= "CREATE TABLE IF NOT EXISTS imgs(dateid INTEGER, place TEXT, address TEXT, image BLOB)"
    c.execute(stmt)

    close_db()
    return
#=====================================


#CREATE AN ACCOUNT
#-------------------------------------
def create_acc(user, first, last, email, birthday, pwd1, pwd2, zipcode):
    global db
    try:
        user=user.strip().lower()
        c = open_db()
        #hashing pwd
        obj = hashlib.sha224(pwd1)
        hash_pwd = obj.hexdigest()

        command = "INSERT INTO accounts VALUES(?,?,?,?,?,?,?)"
        c.execute(command, (user, first, last, email, birthday, hash_pwd, zipcode)) #try to see if user exists
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


#setup()


'''testing'''
#print create_acc("crashley", "bubba", "bubba", 10000)
#print auth("crashley", "bobba")
#print auth("crashley", "bubba")
'''
likes = ["happiness", "butter", "butterflies", "good mac and cheese", "sing", "song", "sing"]
for entry in likes:
    add_interest("crashley", entry)
'''
    
#GET INTEREST (FOR EVENTBRITE)
#----------------------------------------
def get_interest(user):
    global db
    try:
        user = user.strip().lower()
        c = open_db()

        command = "SELECT like FROM likes WHERE user=?"
        res = c.execute(command, (user,))
        likes = []
        for obj in res:
            likes.append(obj[0])
        close_db()
    except:
        print "Error: could not make call on interest"
        return (False,likes)
    return (True, likes)
#=========================================  

setup()
'''more testing
ash = get_interest("crashley")
if (ash[0]):
    print ash[1]
    open_db()
    for obj in ash[1]:
        print obj
else:
    print ash[0]
'''


#GET USERS
#-----------------------------------------
def get_users():
    global db
    try:
        c = open_db()

        command = "SELECT user FROM accounts"
        res = c.execute(command)
        users = []
        for user in res:
            users.append(user[0])
        close_db()
    except:
        print "Error: could not get list of users"
        return (False,users)
    return (True,users)
#==========================================

#testing
'''
create_acc("annie", "woooo", "woooo", 11223)
create_acc("Stuy", "vesant", "vesant", 11228)
create_acc("notStuy", "HS", "HS", 11220)
'''
'''
res = get_users()
print res[1]
'''

#GET ZIPCODE
#-----------------------------------------
def get_zipcode(username):
    global db
    try:
        c = open_db()

        command = "SELECT * FROM accounts"
        res = c.execute(command)
        users = []
        for user in res:
            if user[0] == username:
                return user[7]
        close_db()

    except:
        return "Could not access zipcode"

#get_zipcode("abc123") 
#==========================================

#GET FIRSTNAME
#-----------------------------------------
def get_firstname(username):
    global db
    try:
        c = open_db()

        command = "SELECT * FROM accounts"
        res = c.execute(command)
        users = []
        for user in res:
            if user[0] == username:
                return user[1]
        close_db()

    except:
        return "Could not access firstname"

#==========================================

#GET LASTNAME
#-----------------------------------------
def get_lastname(username):
    global db
    try:
        c = open_db()

        command = "SELECT * FROM accounts"
        res = c.execute(command)
        users = []
        for user in res:
            print user
            print user[2]
            if user[0] == username:
                return user[2]
        close_db()

    except:
        return "Could not access lastname"

#==========================================

#GET EMAIL
#-----------------------------------------
def get_email(username):
    global db
    try:
        c = open_db()

        command = "SELECT * FROM accounts"
        res = c.execute(command)
        users = []
        for user in res:
            if user[0] == username:
                return user[3]
        close_db()

    except:
        return "Could not access email"

#==========================================

#GET BIRTHDAY
#-----------------------------------------
def get_birthday(username):
    global db
    try:
        c = open_db()

        command = "SELECT * FROM accounts"
        res = c.execute(command)
        users = []
        for user in res:
            if user[0] == username:
                return user[4]
        close_db()

    except:
        return "Could not access birthday" 
#==========================================


#CONNECT USERS (USER1 initiates connection)
#------------------------------------------
def connect(user1,user2):
    global db
    try:
        c = open_db()

        command = "INSERT INTO ships VALUES(NULL,?,?,0,0)"
        c.execute(command, (user1,user2))
        close_db()
    except:
        print "Error: could not connect users"
        return False
    return True
#===========================================
#print connect("crashley","annie")
#print connect("crashely","gator")
#print connect("crashley","idkanymore")
#print connect("annabeth","crashley")


#CHECK CONNECTIONS (WHO USER IS CONNECTED TO)
#-------------------------------------------
def check_connect(user):
    global db
    try:
        c = open_db()
        command = "SELECT * FROM ships WHERE user1=? AND status=1"
        res = c.execute(command, (user,))
        lst1 = []
        for obj in res:
            lst1.append(obj)
        command = "SELECT * FROM ships WHERE user2=? AND status=1"
        res = c.execute(command, (user,))
        lst2 = []
        for obj in res:
            lst2.append(obj)
        command = "SELECT * FROM ships WHERE user2=? AND status=0"
        res = c.execute(command, (user,))
        lst3 = []
        for obj in res:
            lst3.append(obj)
        lst1.extend(lst2)
        close_db()
    except:
        print "Error: could not pull connections"
        return []
    return {"confirmed":lst1,"pending": lst3}
#===========================================

#print check_connect("crashley")

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

#print respond(3,1)

#FIND RELATIONSHIP BETWEEN TWO USERS
#--------------------------------------------
def get_relationship(user1,user2):
    global db
    try:
        c = open_db()

        command = "SELECT * FROM ships WHERE user1 = ? AND user2 = ?"
        res1 = c.execute(command, (user1,user2))
        lst1 = []
        for obj in res1:
            lst1.append(obj)
        command = "SELECT * FROM ships WHERE user2 = ? AND user1 = ?"
        res2 = c.execute(command, (user1,user2))
        for obj in res2:
            lst1.append(obj)
        ship = lst1[0]
        shipid = ship[0]

        command = "SELECT * FROM dates WHERE shipid =?"
        res = c.execute(command, (shipid,))
        dates = []
        for obj in res:
            dates.append(obj)

    except:
        print "Error: could not get details"
        return []
    return [ship, dates]
#==============================================

#print get_relationship("crashley","idkanymore")

#----------------------------------------------
def update_pts(shipid, points):
    global db
    try:
        c = open_db()

        command = "SELECT pts FROM ships WHERE shipid = ?"
        res = c.execute(command, (shipid,))
        current_pts = []
        for obj in res:
            current_pts.append(obj)
        new_pts = current_pts[0][0] + points
        print new_pts
        
        command = "UPDATE ships SET pts = ? WHERE shipid = ?"
        c.execute(command, (new_pts,shipid))
        close_db()
    except:
        print "Error: could not update pts"
        return False
    return True
#==============================================
#print update_pts(3, 20)

#----------------------------------------------
def start_date(shipid,date):
    global db
    try:
        c = open_db()

        command = "INSERT INTO dates VALUES(NULL,?,?,1)"
        c.execute(command, (date, shipid))

        close_db()
    except:
        print "Error: could not start date"
        return False
    return True
#===============================================
#print start_date(3, "Wednesday")


#-----------------------------------------------
def complete_date(dateid):
    global db
    try:
        c = open_db()

        command = "UPDATE dates SET status = 0 WHERE dateid = ?"
        c.execute(command, (dateid,))

        close_db()
    except:
        print "Error: could not end date"
        return False
    return True
#==============================================
#print complete_date(1);


#----------------------------------------------
def add_event(dateid, event, location, time):
    global db
    try:
        c = open_db()

        command = "INSERT INTO planner VALUES(?,?,?,?)"
        c.execute(command, (dateid,event,location,time))
        close_db()
    except:
        print "Error: could not add event"
        return False
    return True
#===============================================

#print add_event(2,"skiing", "park", "sometime")
#print add_event(2,"this", "WILL", "be more official, promise")
#print add_event(2,"movies", "amc", "sunday afternoon")

#-----------------------------------------------
def get_plan(dateid):
    global db
    try:
        c = open_db()

        command = "SELECT * FROM planner WHERE dateid=?"
        res = c.execute(command, (dateid,))
        events = []
        for obj in res:
            events.append(obj)
        
    except:
        print "Error: could not get events"
        return []
    return events
#===============================================
#print get_plan(2)


#-----------------------------------------------
def add_image(dateid, imgfile, place, address):
    global db
    try:
        c = open_db()

        command = "INSERT INTO imgs VALUES(?, ?,?,?)"
        c.execute(command, (dateid, place, address, imgfile))
        close_db()
    except:
        print "Error: could not add image"
        return False
    return True
#================================================


#------------------------------------------------
def get_imgs(dateid):
    global db
    try:
        c= open_db()
        command = "SELECT * FROM imgs WHERE dateid=?"
        res= c.execute(command, (dateid,))
        imgs = []
        for obj in res:
            imgs.append(obj)
    except:
        print "Error: could not get images"
        return []
    return imgs
#================================================


