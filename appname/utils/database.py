#DamnCThatQT
#Donia Tung (PM), Carol Pan, Taylor Wong, Queenie Xiang
#SoftDev2 pd7
#P02 - Fin



''' List of methods
setup() - sets up db

create_acc(user,pwd1,pwd2) - sees if input is valid, adds acc to db
    returns (T/F, T/F) -- (is username valid, is password valid)

auth(user,pwd) - checks if user and pwd match
    returns T/F

'''

global db
import sqlite3
import hashlib

#open database
def open_db():
    global db
    f = "data/dating.db"
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
    c= open_db() #account id?
    stmt= "CREATE TABLE IF NOT EXISTS accounts(user TEXT PRIMARY KEY, pass TEXT, likes TEXT, dislikes TEXT)"
    c.execute(stmt)

    close_db()
    return
#=====================================


#CREATE AN ACCOUNT
#-------------------------------------
def create_acc(user, pwd1, pwd2):
    global db
    try:
        user=user.strip().lower()
        c = open_db()
        #hashing pwd
        obj = hashlib.sha224(pwd1)
        hash_pwd = obj.hexdigest()

        command = "INSERT INTO accounts VALUES(?,?,?,?)"
        c.execute(command, (user,hash_pwd,"None yet","None yet")) #try to see if user exists
        #if pwds don't match
        if pwd1 != pwd2:
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
