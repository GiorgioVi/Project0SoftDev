import sqlite3

f="data/story.db"
db = sqlite3.connect(f)
c = db.cursor()
#==========================================================
def help(found):
    for num in found:
        return (num[0] == 1)

def validate(username, password):
    # print ("SELECT count(*) FROM users WHERE username = '%s' AND password = %s" % (username, password))
    found = c.execute("SELECT count(*) FROM users WHERE username = '%s' AND password = '%s'" % (username, password))
    return help(found)

def hasUsername(username):
    # print ("SELECT count(*) FROM users WHERE username = '%s'" % (username))
    found = c.execute("SELECT count(*) FROM users WHERE username = '%s'" % (username))
    return help(found)

def newID():
    # get the max id
    maxID = c.execute("SELECT MAX(id) FROM users")
    for num in maxID:
        # the newest id
        return num[0] + 1

def addUser(username, password):
    c.execute("INSERT INTO users VALUES('%s', '%s', '%s')" % (username, password, newID()))
    
def updatePassword(username, newpass):
    c.execute("UPDATE users SET password = '%s' WHERE username = '%s'" % (newpass, username))

def hasTitle(title):
    found = c.execute("SELECT count(*) FROM storylist WHERE title = '%s'" % (title))
    return help(found)

def hasContributed(userid, storyid):
    found = c.execute("SELECT count(*) FROM useredit WHERE id = %s AND storyid = %s" % (userid, storyid))
    return help(found)

def getStoryTitle(storyid):
    title = c.execute("SELECT title FROM storylist WHERE storyid = %s" % (storyid))
    for t in title:
        return t[0]

def getFullStory(storyid):
    edits = c.execute("SELECT display FROM useredit WHERE storyid = %s" % (storyid))
    story = ""
    for edit in edits:
        story += edit[0]
    print story
    return story

def insertEdit(userid, edit, storyid):
    #add edit to the list of edits
    c.execute("INSERT INTO useredit VALUES(%s, %s, '%s')" % (userid, storyid, edit))
    #updating preexiting story
    c.execute("UPDATE storylist SET id = '%s', display = '%s' WHERE storyid = %s" % (userid, edit, storyid))

def getStoryID(title):
    ids = c.execute("SELECT storyid FROM storylist WHERE title = '%s'" % (title))
    for i in ids:
        return i[0]
    
def getStoryEdit(title):
    edit = c.execute("SELECT display FROM storylist WHERE title = '%s'" % (title))
    for e in edit:
        return e[0]

def getAuthor(title):
    author = c.execute("SELECT id FROM storylist WHERE title = '%s'" % (title))
    for a in author:
        return a[0]
        
#==========================================================
#TESTING
'''
addUser('connie', 'hello');
updatePassword('connie','1234')
'''

#==========================================================

db.commit() #save changes
db.close()  #close database
