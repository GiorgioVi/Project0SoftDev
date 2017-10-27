from flask import Flask, render_template, request, session, redirect, url_for, flash
import os, csv, sqlite3
import db_func

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
    username = request.form["name"]
    password= request.form["pass"]

    status = db_func.validate(username, password)
    
    if status:
        session['user'] = username
    elif db_func.hasUsername(username):
        flash("Wrong password")
    else:
        flash("User doesn't exist")
    return redirect(url_for('root'))

@my_app.route('/registration', methods=['GET','POST'])
def register():
    return render_template("register.html")

@my_app.route('/submitregister', methods= ['GET', 'POST'])
def submitregister():

    username = request.form["newuser"]
    password = request.form["newpass"]

    if (password != request.form["repeatpass"]):
        flash("Your passwords do not match. Please try again.")
        return render_template("register.html")
    else:
        if db_func.hasUsername(username):
            flash("An account with that username already exists. Please try again.")
            return render_template("register.html")
        else:
            db_func.addUser(username, password)
            flash("You have successfully registered your account! You may log in now.")
            return redirect(url_for("root"))

@my_app.route('/loggedout', methods=['GET','POST'])
def logout():
    if ('user' in session):
        session.pop('user')
    return redirect(url_for("root"))

@my_app.route('/home', methods=['GET','POST'])
def home():
    if ('user' in session):
        return render_template("home.html", storiesAddedTo = db_func.getStoriesAddedTo(db_func.getUserID(session['user'])))
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
    if db_func.hasTitle(title):
        flash("Title already exists!")
    else:
        db_func.addStory(db_func.getUserID(session['user']), title, startstory)
        flash("Story has been created!")
    return redirect(url_for("root"))

@my_app.route('/readstory', methods=['GET','POST'])
def read():
    if ('user' in session):
        return render_template("read.html", storiesAddedTo = db_func.getStoriesAddedTo(db_func.getUserID(session['user'])))
    return redirect(url_for("root"))

@my_app.route('/editstory', methods=['GET','POST'])
def edit():
    if ('user' in session):
        return render_template("edit.html", storiesNotAddedTo = db_func.getStoriesAddedTo(db_func.getUserID(session['user'])))
    return redirect(url_for("root"))

@my_app.route('/submitedit', methods=['GET','POST'])
def submitedit():
    title = request.form["newtitle"]
    startstory = request.form["newstory"]
    if db_func.hasTitle(title):
        flash("Title already exists!")
    else:
        db_func.addStory(db_func.getUserID(session['user']), title, startstory)
        flash("Story has been created!")
    return redirect(url_for("root"))

if __name__ == '__main__':
    my_app.debug = True
    my_app.run()

#db.commit()
#db.close()
