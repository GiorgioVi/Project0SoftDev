import sqlite3   #enable control of an sqlite database

f="data/story.db"
db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#==========================================================
def table_gen():
    create_users = "CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, id INTEGER)"
    c.execute(create_users)

    create_useredit = "CREATE TABLE IF NOT EXISTS useredit(id INTEGER, storyid INTEGER, edit TEST)"
    c.execute(create_useredit)

    create_storylist = "CREATE TABLE IF NOT EXISTS storylist(title TEXT, id INTEGER, contributors INTEGER, display TEXT)"
    c.execute(create_storylist)

table_gen()
#==========================================================
db.commit() #save changes
db.close()  #close database
