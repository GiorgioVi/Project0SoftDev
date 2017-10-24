import sqlite3

f="data/story.db"
db = sqlite3.connect(f)
c = db.cursor()
#==========================================================
def validate(username, password):
    # print ("SELECT count(*) FROM users WHERE username = '%s' AND password = %s" % (username, password))
    found = c.execute("SELECT count(*) FROM users WHERE username = '%s' AND password = '%s'" % (username, password))
    for num in found:
        return (num[0] == 1)

def findUsername(username):
    # print ("SELECT count(*) FROM users WHERE username = '%s'" % (username))
    found = c.execute("SELECT count(*) FROM users WHERE username = '%s'" % (username))
    for num in username:
        return (num[0] == 1)

def createNewID():
    #get the max of the id in users.id
    maxID = c.execute("SELECT MAX(id) FROM users")
    for num in maxID:
        return num[0] + 1

def addUser(username, password):
    # print ("INSERT INTO users VALUES(%s, %s, %s)" % (username, password, ))
    c.execute("INSERT INTO users VALUES('%s', '%s', '%s')" % (username, password, 4))
    
def updatePassword(password):
    # print ("UPDATE users SET password = %s" % (password))
    c.execute("UPDATE users SET password = %s" % (password))
#==========================================================

#==========================================================

db.commit() #save changes
db.close()  #close database
