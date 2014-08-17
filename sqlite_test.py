__author__ = 'denislavrov'
import sqlite3
DATABASE = 'test.db'


def createtable():
    conn = sqlite3.connect(DATABASE)
    conn.execute('''
    CREATE TABLE USERS
    (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    USERNAME TEXT NOT NULL,
    PASSWORD TEXT NOT NULL);
    ''')
    conn.close()

def commitdata(username, password):
    conn = sqlite3.connect(DATABASE)
    conn.execute("INSERT INTO USERS (USERNAME, PASSWORD) \
    VALUES ('%s','%s')" % (username, password))
    conn.commit()
    conn.close()

def listuser():
    conn = sqlite3.connect(DATABASE)
    rows = conn.execute("SELECT USERNAME, PASSWORD FROM USERS")
    conn.close()
    return list(rows)

def rmuser(username):
    conn = sqlite3.connect(DATABASE)
    conn.execute("DELETE FROM USERS WHERE USERNAME='%s'" % username)
    conn.commit()
    conn.close()

def userexists(username):
    conn = sqlite3.connect(DATABASE)
    rows = conn.execute("SELECT USERNAME FROM USERS WHERE USERNAME='%s'" % username)
    if list(rows).__contains__((username,)):
        retval = True
    else:
        retval = False
    conn.close()
    return(retval)



