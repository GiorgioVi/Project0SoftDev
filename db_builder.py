import sqlite3   #enable control of an sqlite database

f="data/story.db"
db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#==========================================================
def table_gen():
    create_users = "CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, id INTEGER)"
    c.execute(create_users)

    create_useredit = "CREATE TABLE IF NOT EXISTS useredit(id INTEGER, storyid INTEGER, edit TEXT)"
    c.execute(create_useredit)

    create_storylist = "CREATE TABLE IF NOT EXISTS storylist(title TEXT, id INTEGER, storyid INTEGER, display TEXT)"
    c.execute(create_storylist)

def default():
    # commands do not run unless it is the start
    # really not necessary unless someone wants to run db_builder more than once...
    for status in c.execute("SELECT count(*) FROM users WHERE username = 'admin' AND password = 'password'"):
        if(status[0] != 1):     
            c.execute("INSERT INTO users VALUES('%s', '%s', 0)" % ('admin', 'password'))
            c.execute("INSERT INTO storylist VALUES('%s', 0, 0, '%s')" % ('template', 'a story'))
            c.execute("INSERT INTO useredit VALUES(0, 0, 'a story')")
            return
              
table_gen()
default()
#==========================================================
db.commit() #save changes
db.close()  #close database
