from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from os import getenv
import re 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///messages.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Message(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), nullable = False)
    subject = db.Column(db.String(50), nullable = False)
    message = db.Column(db.String(300), nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return (self.email, ' ', self.subject)

@app.route('/')
def home():
    return render_template('home.html', title = 'Home')

@app.route('/projects')
def projects():
    return render_template('projects.html', title = 'Projects')

@app.route('/art')
def art():
    return render_template('art.html', title = 'Art')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if(username == getenv("USER") and password == getenv("PASS")):
            msgs = Message.query.all()
            return render_template('messages.html', title = 'Messages', msgs = msgs)
    return render_template('login.html', title = 'Admin')

@app.route('/contact', methods=['GET', 'POST'])
def contact():

    error = {
        "email": "",
        "subject": "",
        "message": ""
    }

    if request.method == "POST":
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if(len(email) == 0 or re.search(email, regex) == False):
            error["email"] = "Please enter a valid email"
        elif(len(subject) == 0 and len(subject) <= 50):
            error["subject"] = "This field is required"
        elif(len(message) == 0 and len(message) <= 300):
            error["message"] = "This field is required"
        else:
            message = Message(email = email, subject = subject, message = message)
            db.session.add(message)
            db.session.commit()
            return render_template('contact.html', title = 'Contact', errors = error, success = True)
        

    return render_template('contact.html', title = 'Contact', errors = error)

    
if __name__ == '__main__':
	app.run(debug=True)