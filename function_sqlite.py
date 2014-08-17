__author__ = 'denislavrov'

import sqlite3  # used for database handling
import hashlib  # used for password hashing
from getpass import getpass  # used for getting passwords without echoing input
import sys  # used to display error information in exceptions


DATABASE = 'test.db'  # global database for functions to operate with
cUser = ""  # current user of the shell


def checkuser(username, hash):
    for i in readusers():
        if i[0] == username and i[1] == hash:
            return True
    return False


def createtable(filename=''):  # function called to insert a table into a new database
    conn = sqlite3.connect(filename)  # opening/connecting to a database just like a file
    # following is the statement in SQL, to create such table, with ID field that is automatically incremented
    # username and password fields that are NOT NULL values.
    conn.execute('''CREATE TABLE USERS
       (ID INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
       USERNAME TEXT    NOT NULL,
       PASSWORD TEXT     NOT NULL
       );
       ''')
    conn.close()  # and closing the database after done with our modification, just like with a file.


def createdb(filename=''):  # this function actually creates a physical file, for database to be stored in
    if filename == '':  # since some functions may be used just to reuse code they have keys to avoid user input
        while (len(filename) == 0) or (filename[len(filename) - 3:len(filename)] != '.db'):
            # check that input is not emtpy and ends with .db
            filename = input("Please enter a filename that ends with '.db': ")
    try:  # check if database exists by trying to open it for reading
        open(filename, mode='r')  # if file exists the following code is not run and jump to 'except:' is made.
        while 1:  # if database does exist ask user if he would like to switch to it
            useri = input("This database already exists. Would you like to switch to it? [Y,N]: ").lower()
            if useri == 'y':
                switchdb(filename=filename)  # invoke function to switch
                break
            elif useri == 'n':  # if user chooses not to switch send him back recursively,by calling this function again
                createdb()
                break
    except IOError:  # if file does not exist, then create it, create the table in it and switch to it.
        open(filename, mode='a').close()  # a quick way to create an empty file in one line.
        createtable(filename=filename)
        switchdb(filename=filename)


def switchdb(filename=''):  # a function to switch databases
    while 1:
        if filename == '':  # check for a preset key as usual if not set ask user for input
            filename = input("Please input a valid existing database name: ")
        try:  # try to open database for reading just to check that the file is there
            file = open(filename, mode='r')
        except IOError:
            print("Error switching the database.")
        else:  # no exception raised everything is fine, set that database to current database and reset current user
            global cUser, DATABASE
            cUser = ''
            DATABASE = filename
            file.close()
            break


def insertuser(username, password):  # little function to insert a new user into the database
    conn = sqlite3.connect(DATABASE)
    conn.execute("INSERT INTO USERS (USERNAME, PASSWORD) \
    VALUES ('%s','%s')" % (username, password))
    conn.commit()  # when inputting data into the database you must call commit() method before closing
    conn.close()


def checkdb(db, create=False):  # helper function to check if database exists
                                # could be expanded to check data inside database
    try:
        open(db, mode='r').close()
        return True
    except IOError:
        print("Database %s does not exist, please create one." % db)
        if create:
            createdb()
        else:
            return False


def readusers():  # read the users in from the database
    conn = sqlite3.connect(DATABASE)
    rows = conn.execute("SELECT USERNAME, PASSWORD FROM USERS")
    lrows = list(rows)
    conn.close()
    return lrows


def listuser():  # display the users from format of readusers() function
    print("%-20s %-20s" % ("Username:", "Hash:"))
    for i in readusers():
        print("%-20s %-20s" % (i[0], i[1]))


def rmuser(username=''):  # function to remove a user
    global cUser
    if username == '':
        username = input("Please enter username to remove: ")
    conn = sqlite3.connect(DATABASE)
    conn.execute("DELETE FROM USERS WHERE USERNAME='%s'" % username)
    conn.commit()  # must commit when making changes
    conn.close()
    if username == cUser:  # if current user is the user being deleted set current user to no one
        cUser = ''
    return username


def encrypt(salt, password):  # function to hash the password with salt, common salt is the username
    return hashlib.sha512((salt + password).encode()).hexdigest()


def updaterec(uid=0, username='', password=''):  # function to update the records based on parameters given
    if uid == 0 and username != '':
        uid = getid(username)  # if user id is not given, but username is, try to find uid
    if (uid != 0) and (username != '' or password != ''):  # if uid is known and password or username given update them
        conn = sqlite3.connect(DATABASE)
        if username != '' and password == '':
            conn.execute("UPDATE USERS set USERNAME = '%s' where ID=%d" % (username, uid))  # update username only
        elif password != '' and username == '':
            conn.execute("UPDATE USERS set PASSWORD = '%s' where ID=%d" % (password, uid))  # update password only
        else:  # and update both
            conn.execute("UPDATE USERS set USERNAME = '%s', PASSWORD = '%s' where ID=%d" % (username, password, uid))
        conn.commit()
        conn.close()


def getid(username):  # helper function to getid of user by username
    conn = sqlite3.connect(DATABASE)
    uid = list(conn.execute("SELECT ID FROM USERS WHERE USERNAME='%s'" % username))[0][0]
    conn.close()
    return uid


def passwd(username='', password=''):  # function to change the password of a user, supports being given parameters.
    if username == '' or password == '':  # if parameters aren't given ask user
        username = input("Please enter a username: ")
        password = encrypt(username, getpass(prompt="Please enter password for %s:" % username))
        if checkuser(username, password):  # check that username and password are matching
            password = getpass(prompt="Please enter the new password for %s:" % username)  # ask for new password
            if password == getpass(prompt="Please enter the new password again:"):
                updaterec(username=username, password=encrypt(username, password))  # after verifying password update it
            else:
                print("Passwords do not match please try again.")
        else:
            print("Username or password were incorrect.")
    elif userexists(username):
        updaterec(username=username, password=encrypt(username, password))  # or just update if given as parameters
    else:
        print("User %s does not exist!" % username)


def userexists(username):  # helper function to check if the user exists
    conn = sqlite3.connect(DATABASE)
    rows = list(conn.execute("SELECT USERNAME FROM USERS WHERE USERNAME='%s'" % username))
    conn.close()
    return rows.__contains__((username,))


def adduser(username='', password=''):  # function to add a user
    if username == '':  # check to see if key argument is set
        username = input("Please enter a username: ")
    if not userexists(username):
        if password == '':
            password = getpass(prompt="Please enter password for %s:" % username)  # ask user for password twice
            if password != getpass(prompt="Please enter the password again:"):
                print("Passwords do not match please try again")
                return
        insertuser(username, encrypt(username, password))  # add a user if arguments were passed or entered by user

    else:
        print("User %s already exists. Please choose another username." % username)  # print error if new user exists


def login(username=''):
    if username == '':
        username = input("Please enter a username: ")
    hash = encrypt(username, getpass(prompt="Please enter password for %s:" % username))
    global cUser
    if checkuser(username, hash):
        cUser = username
    else:
        print("Login failed.")


def logout():
    global cUser
    cUser = ''


def shell():  # function that facilitates an interactive python shell
    while 1:
        useri = input("#" + DATABASE + "#" + cUser + "!>")  # continuously ask for user input
        if useri == 'exit':  # exit, exits the shell
            break
        else:
            try:
                exec(useri)  # try to execute user input if it fails, just print there was an error.
            except:
                print("Error: %s" % sys.exc_info()[0])
