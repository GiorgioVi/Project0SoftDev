from flask import Flask, render_template, request, session, redirect, url_for, flash
import os, csv

my_app = Flask(__name__)
my_app.secret_key = os.urandom(32)

logindict = {}

with open('data/logins.csv', mode='r') as infile:
    reader = csv.reader(infile)
    logindict = {rows[0]:rows[1] for rows in reader}

@my_app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('login.html')

@my_app.route('/registration', methods=['GET','POST'])
def register():
    return render_template("register.html")

@my_app.route('/submitregister', methods= ['GET', 'POST'])
def submitregister():
    username = request.form["newuser"]
    passwrd = request.form["newpass"]
    if (passwrd != request.form["repeatpass"]):
        flash("Your passwords do not match. Please try again.")
        return render_template("register.html")
    else:
        if (username not in logindict):
            logindict[username] = passwrd
            with open('data/logins.csv','a') as f:
                w = csv.writer(f)
                w.writerow([username,passwrd])
                f.close()
                flash("You have successfully registered your account! You may log in now.")
                return redirect(url_for("root"))
        else:
            flash("An account with that username already exists. Please try again.")
            return render_template("register.html")

if __name__ == '__main__':
    my_app.debug = True
    my_app.run()

