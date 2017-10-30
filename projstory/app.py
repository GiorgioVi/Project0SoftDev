from flask import Flask, render_template, request, session, redirect, url_for, flash
import os, csv, sqlite3, hashlib
import db_func

my_app = Flask(__name__)
my_app.secret_key = os.urandom(32)

#========================LOGIN/ACCOUNT STUFF============================
@my_app.route('/', methods=['GET', 'POST'])
def root():
    return redirect(url_for("login"))

@my_app.route("/login", methods =['GET','POST'])
def login():
    if 'user' in session:
        ID = db_func.getID(session['user'])
        print (db_func.getStoriesNotAddedTo(ID))
        return render_template("home.html", view = db_func.getStoriesAddedTo(ID), edit = db_func.getStoriesNotAddedTo(ID))
    else:
        if (request.method == 'GET'):
            return render_template('login.html')
        else:
            username = request.form["username"]
            password = request.form["password"]
            hash_obj = hashlib.sha256(password)
            hex_dig = hash_obj.hexdigest()
            status = db_func.validate(username, hex_dig)
            if status:
                session["user"] = username
            elif db_func.hasUsername(username):
                flash("Incorrect credentials.")
            else:
                flash("Username does not exist.")
            return redirect(url_for('login'))

@my_app.route('/register', methods=['GET','POST'])
def register():
    if (request.method == 'POST'):
        username = request.form["newUsername"]
        password = request.form["newPassword"]
        repeat = request.form["repeatPassword"]
        if(password != repeat):
            flash("Passwords do not match.")
        else:
            if db_func.hasUsername(username):
                flash("Username taken.")
            else:
                hash_obj = hashlib.sha256(password)
                hex_dig = hash_obj.hexdigest()
                db_func.addUser(username, hex_dig)
                flash("Your account has been registered.")
                return redirect(url_for("login"))
    return render_template("register.html")

@my_app.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
        flash("Logged out.")
    return redirect(url_for('login'))
#=======================================================================

#===========================STORY STUFF=================================

@my_app.route('/create', methods=['GET','POST'])
def create():
    if ('user' in session):
        if (request.method == "POST"):
            title = request.form["title"]
            edit = request.form["edit"]
            if db_func.hasTitle(title):
                flash("Title already exists!")
                return render_template("create.html")
            else:
                userID = db_func.getID(session['user'])
                db_func.addStory(userID, title, edit)
                flash("Story has been created.")
                return redirect(url_for('login'))
        return render_template("create.html")
    flash("Please login.")
    return redirect(url_for("login"))

@my_app.route('/view', methods=['GET','POST'])
def view():
    if (request.method == "GET"):
        flash("Whatcha doing here? There's no story to view.")
        return redirect(url_for("login"))
    elif ('user' in session):
        ID = request.form["storyID"]
        fullStory = db_func.getStory(ID)
        title = db_func.getTitle(ID)
        return render_template('view.html', title = title, fullStory = fullStory)
    else:
        flash("Please login.")
        return redirect(url_for("login"))

@my_app.route('/edit', methods =['POST'])
def edit():
    if('user' in session):
        ID = request.form["storyID"]
        return render_template('edit.html', title =  db_func.getTitle(ID), display = db_func.getEdit(ID), ID = ID)
    else:
        flash("Please login.")
        return redirect(url_for("login"))

@my_app.route('/editing', methods=['POST'])
def editted():
    if ('user' in session):
        ID = request.form["storyID"]
        display = db_func.getEdit(ID)
        if(len(request.form["edit"]) < 50):
            userID = db_func.getID(session['user'])
            db_func.insertEdit(userID, request.form["edit"], ID)
            flash("Added to story.")
            return redirect(url_for('login'))
        else:
            flash("Only 50 characters allowed.")
            return render_template("edit.html",title = db_func.getTitle(ID), display = db_func.getEdit(ID), ID = ID)
    else:
        flash("Please login.")
        return redirect(url_for("login"))

if __name__ == '__main__':
    my_app.debug = True
    my_app.run()
