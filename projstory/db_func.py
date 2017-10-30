import sqlite3

f="data/story.db"
#==========================================================

def validate(username, password):
    db = sqlite3.connect(f)
    c = db.cursor()
    # print ("SELECT count(*) FROM users WHERE username = '%s' AND password = %s" % (username, password))
    found = c.execute("SELECT count(*) FROM users WHERE username = '%s' AND password = '%s'" % (username, password)).fetchall()
    db.commit()
    db.close()
    return (found[0][0] == 1)

def hasUsername(username):
    db = sqlite3.connect(f)
    c = db.cursor()
    # print ("SELECT count(*) FROM users WHERE username = '%s'" % (username))
    found = c.execute("SELECT count(*) FROM users WHERE username = '%s'" % (username)).fetchall()
    db.commit()
    db.close()
    return (found[0][0] == 1)

def newID():
    db = sqlite3.connect(f)
    c = db.cursor()
    # get the max id
    maxID = c.execute("SELECT MAX(id) FROM users").fetchall()
    db.commit()
    db.close()
    return maxID[0][0] + 1

def newStoryID():
    db = sqlite3.connect(f)
    c = db.cursor()
    # get the max id
    maxID = c.execute("SELECT MAX(storyid) FROM storylist").fetchall()
    db.commit()
    db.close()
    return maxID[0][0] + 1

def addUser(username, password):
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute("INSERT INTO users VALUES('%s', '%s', '%s')" % (username, password, newID()))
    db.commit()
    db.close()

def getID(username):
    db = sqlite3.connect(f)
    c = db.cursor()
    ids = c.execute("SELECT id FROM users WHERE username = '%s'" % (username)).fetchall()
    db.commit()
    db.close()
    return ids[0][0]
    
def hasTitle(title):
    db = sqlite3.connect(f)
    c = db.cursor()
    found = c.execute("SELECT count(*) FROM storylist WHERE title = '%s'" % (title))
    for num in found:
        db.commit()
        db.close()
        return (num[0] == 1)

def addStory(id, title, text):
    db = sqlite3.connect(f)
    c = db.cursor()
    storyid = newStoryID()
    c.execute("INSERT INTO storylist VALUES('%s', '%s', '%s', '%s')" % (title, id, storyid, text))
    c.execute("INSERT INTO useredit VALUES('%s', '%s', '%s')" % (id, storyid, text))
    db.commit()
    db.close()

def getStoriesAddedTo(userid):
    db = sqlite3.connect(f)
    c = db.cursor()
    storyIDs = c.execute("SELECT useredit.storyid, storylist.title, useredit.edit FROM useredit, storylist WHERE useredit.id == %s AND storylist.storyid = useredit.storyid" % (userid)).fetchall()
    db.commit()
    db.close()
    return storyIDs

def getStoriesNotAddedTo(userid):
    db = sqlite3.connect(f)
    c = db.cursor()
    storyIDs = c.execute("SELECT DISTINCT storyid FROM useredit WHERE id != %s AND storyid NOT IN (SELECT storyid FROM useredit WHERE id == %s)" % (userid, userid)).fetchall()
    i = 0
    while(i < len(storyIDs)):
        dets = c.execute("SELECT title, display FROM storylist WHERE storyid == %s" % (storyIDs[i][0])).fetchall()
        storyIDs[i] += dets[0]
        i += 1
    db.commit()
    db.close()
    return storyIDs

def getStoryID(title):
    db = sqlite3.connect(f)
    c = db.cursor()
    s = c.execute("SELECT storyid FROM storylist WHERE title = '%s'" % (title)).fetchall()
    print s
    db.commit()
    db.close()
    return s[0][0]

def getTitle(storyid):
    db = sqlite3.connect(f)
    c = db.cursor()
    t = c.execute("SELECT title FROM storylist WHERE storyid = %s" % (storyid)).fetchall()
    db.commit()
    db.close()
    return t[0][0]

def getStory(storyid):
    db = sqlite3.connect(f)
    c = db.cursor()
    edits = c.execute("SELECT edit FROM useredit WHERE storyid = %s" % (storyid)).fetchall()
    story = ""
    for edit in edits:
        story += edit[0] + " "
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

def getEdit(storyID):
    db = sqlite3.connect(f)
    c = db.cursor()
    edit = c.execute("SELECT display FROM storylist WHERE storyid = '%s'" % (storyID)).fetchall()
    db.commit()
    db.close()
    return edit[0][0]
    
'''
def updatePassword(username, newpass):
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute("UPDATE users SET password = '%s' WHERE username = '%s'" % (newpass, username))
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
    
def getAuthor(title):
    db = sqlite3.connect(f)
    c = db.cursor()
    author = c.execute("SELECT id FROM storylist WHERE title = '%s'" % (title))
    for a in author:
        db.commit()
        db.close()
        return a[0]
'''
#==========================================================
#TESTING
print(getStoryID('testing for admin'))
#==========================================================
