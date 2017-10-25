from flask import Flask, render_template, request, session, redirect, url_for, flash
import os, csv, sqlite3

my_app = Flask(__name__)
my_app.secret_key = os.urandom(32)

@my_app.route('/', methods=['GET', 'POST'])
def root():
    if ('user' in session):
        #return render_template('welcome.html', name = session['user'])
        return redirect(url_for("home"))
    return render_template('login.html')

@my_app.route('/submitted', methods=['GET','POST'])
def submitted():

    f = "data/story.db"
    db =  sqlite3.connect(f)
    c = db.cursor()

    username = request.form["name"]
    passwrd= request.form["pass"]

    if inList(username, c.execute("SELECT username FROM users")):
        if (passwrd == getPass(username, c.execute("SELECT username, password FROM users"))):
            session['user'] = username
        else:
            flash("Wrong password")
    else:
        flash("User doesn't exist")
    db.commit()
    db.close()
    return redirect(url_for('root'))

def inList(newuser, dbobj):
    for x in dbobj:
        if x[0] == newuser:
            return True
    return False

def getPass(username, dbobj):
    for x in dbobj:
        if (x[0] == username):
            return x[1]

@my_app.route('/registration', methods=['GET','POST'])
def register():
    return render_template("register.html")

@my_app.route('/submitregister', methods= ['GET', 'POST'])
def submitregister():

    f = "data/logins.db"
    db =  sqlite3.connect(f)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS login (user TEXT, pass NUMERIC)")

    username = request.form["newuser"]
    passwrd = request.form["newpass"]

    if (passwrd != request.form["repeatpass"]):
        flash("Your passwords do not match. Please try again.")
        return render_template("register.html")
    else:
        if notInList(username, c.execute("SELECT user FROM login")):
            c.execute("INSERT INTO login VALUES (\"%s\",\"%s\");"%(username, passwrd))
            flash("You have successfully registered your account! You may log in now.")
            db.commit()
            db.close()
            return redirect(url_for("root"))
        else:
            flash("An account with that username already exists. Please try again.")
            return render_template("register.html")

def notInList(newuser, dbobj):
    for x in dbobj:
        if x[0] == newuser:
            return False
    return True

@my_app.route('/loggedout', methods=['GET','POST'])
def logout():
    if ('user' in session):
        session.pop('user')
    return redirect(url_for("root"))

@my_app.route('/home', methods=['GET','POST'])
def home():
    if ('user' in session):
        return render_template("home.html")
    return redirect(url_for("root"))

@my_app.route('/createstory', methods=['GET','POST'])
def create():
    if ('user' in session):
        return render_template("create.html")
    return redirect(url_for("root"))

@my_app.route('/submitcreate', methods=['GET','POST'])
def submitcreate():
    title = request.form["newtitle"]
    startstory = request.form["newstory"]

    return redirect(url_for())

if __name__ == '__main__':
    my_app.debug = True
    my_app.run()

db.commit()
db.close()
