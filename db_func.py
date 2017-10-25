import sqlite3

f="data/story.db"
#==========================================================
def help(found):
    for num in found:
        return (num[0] == 1)

def validate(username, password):
    db = sqlite3.connect(f)
    c = db.cursor()
    # print ("SELECT count(*) FROM users WHERE username = '%s' AND password = %s" % (username, password))
    found = c.execute("SELECT count(*) FROM users WHERE username = '%s' AND password = '%s'" % (username, password))
    db.commit()
    db.close()
    return help(found)

def hasUsername(username):
    db = sqlite3.connect(f)
    c = db.cursor()
    # print ("SELECT count(*) FROM users WHERE username = '%s'" % (username))
    found = c.execute("SELECT count(*) FROM users WHERE username = '%s'" % (username))
    db.commit()
    db.close()
    return help(found)

def newID():
    db = sqlite3.connect(f)
    c = db.cursor()
    # get the max id
    maxID = c.execute("SELECT MAX(id) FROM users")
    for num in maxID:
        # the newest id
        db.commit()
        db.close()
        return num[0] + 1

def addUser(username, password):
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute("INSERT INTO users VALUES('%s', '%s', '%s')" % (username, password, newID()))
    db.commit()
    db.close()
    
def updatePassword(username, newpass):
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute("UPDATE users SET password = '%s' WHERE username = '%s'" % (newpass, username))
    db.commit()
    db.close()

def hasTitle(title):
    db = sqlite3.connect(f)
    c = db.cursor()
    found = c.execute("SELECT count(*) FROM storylist WHERE title = '%s'" % (title))
    return help(found)

def hasContributed(userid, storyid):
    db = sqlite3.connect(f)
    c = db.cursor()
    found = c.execute("SELECT count(*) FROM useredit WHERE id = %s AND storyid = %s" % (userid, storyid))
    return help(found)

def getStoryTitle(storyid):
    db = sqlite3.connect(f)
    c = db.cursor()
    title = c.execute("SELECT title FROM storylist WHERE storyid = %s" % (storyid))
    for t in title:
        db.commit()
        db.close()
        return t[0]

def getFullStory(storyid):
    db = sqlite3.connect(f)
    c = db.cursor()
    edits = c.execute("SELECT display FROM useredit WHERE storyid = %s" % (storyid))
    story = ""
    for edit in edits:
        story += edit[0]
        print story
    db.commit()
    db.close()
    return story

def insertEdit(userid, edit, storyid):
    db = sqlite3.connect(f)
    c = db.cursor()
    #add edit to the list of edits
    c.execute("INSERT INTO useredit VALUES(%s, %s, '%s')" % (userid, storyid, edit))
    #updating preexiting story
    c.execute("UPDATE storylist SET id = '%s', display = '%s' WHERE storyid = %s" % (userid, edit, storyid))
    db.commit()
    db.close()
    
def getStoryID(title):
    db = sqlite3.connect(f)
    c = db.cursor()
    ids = c.execute("SELECT storyid FROM storylist WHERE title = '%s'" % (title))
    for i in ids:
        db.commit()
        db.close()
        return i[0]
    
def getRecentEdit(title):
    db = sqlite3.connect(f)
    c = db.cursor()
    edit = c.execute("SELECT display FROM storylist WHERE title = '%s'" % (title))
    for e in edit:
        return e[0]

def getAuthor(title):
    db = sqlite3.connect(f)
    c = db.cursor()
    author = c.execute("SELECT id FROM storylist WHERE title = '%s'" % (title))
    for a in author:
        db.commit()
        db.close()
        return a[0]
    
#==========================================================
#TESTING

#==========================================================
