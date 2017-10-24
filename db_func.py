import sqlite3

f="data/story.db"
db = sqlite3.connect(f)
c = db.cursor()
#==========================================================
def checkCreds(username, password):
    # print ("SELECT count(*) FROM users WHERE username = '%s' AND password = %s" % (username, password))
    numbers = c.execute("SELECT count(*) FROM users WHERE username = '%s' AND password = '%s'" % (username, password))
    for num in numbers:
        return (num[0] == 1)

def checkUsername(username):
    # print ("SELECT count(*) FROM users WHERE username = '%s'" % (username))
    numbers = c.execute("SELECT count(*) FROM users WHERE username = '%s'" % (username))
    for num in numbers:
        return (num[0] == 1)

'''
def getNewID():
    #get the max of the id in users.id
    c.execute("SELECT ")
    for num in numbers:
        return num[]
'''

def addUser(username, password):
    # print ("INSERT INTO users VALUES(%s, %s, %s)" % (username, password, ))
    c.execute("INSERT INTO users VALUES('%s', '%s', '%s')" % (username, password, getNewId()))
    
def updatePassword(password):
    # print ("UPDATE users SET password = %s" % (password))
    c.execute("UPDATE users SET password = %s" % (password))
#==========================================================

addUser("hope", "life")
print(checkCreds("hope","life"))

#==========================================================

db.commit() #save changes
db.close()  #close database
