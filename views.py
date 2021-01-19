from datetime import datetime
from database import Database

from flask import current_app, render_template, session, g
from flask import request, redirect, url_for, flash
from flask_login import current_user
from club import Club
from flask_login import UserMixin, LoginManager, logout_user, login_user, current_user, login_required
from user import get_user, is_user, get_user_club, user_get, user_get_club
from user import User
from event import Event
from forms import LoginForm
from passlib.hash import pbkdf2_sha256 as hasher
from passlib.hash import sha256_crypt
from wtforms import Form, BooleanField, TextField, PasswordField, validators, IntegerField, DateField, DateTimeField, TextAreaField
from os.path import expanduser
import os
import psycopg2
import sqlite3 as dbapi2
import datetime


#from ftforms import Form
#password = "adminpw"
#hashed = hasher.hash(password)
#user_available = False
user_email = ""
club_user = False
student_user = False


def home_page():
    #user_available = False
    return render_template("home.html", user_email = user_email, club_user=club_user, student_user=student_user)


def club_edit_page(): 
    db = current_app.config["db"]
    
    
    

class CommentForm(Form): 

    comment = TextAreaField('Comment', [validators.Length(min=2, max=200)])
    name = TextField('Name', [validators.Length(min=2, max = 50)])
    vote = IntegerField()
    vote = IntegerField('Vote of this event(1-10)', [validators.NumberRange(min=1, max=10)])

#def eclubs_page():
  #  db = current_app.config["db"]
   # clubs = db.get_clubs()
    #return render_template("server.html", clubs = sorted(clubs))

def comment_page(): 
    db.current_app.config["db"]
    form = CommentForm(request.form)
    if request.method == "POST" and form.validate():
        comment = form.comment.data
        name = form.name.data
        vote = form.vote.data
        #db.add_comment(comment, name, vote)      
        
    return redirect("an_event_page",form=form, user_email=user_email, student_user=student_user, club_user=club_user)

def about_page():
    return render_template("about.html", user_email = user_email,club_user=club_user, student_user=student_user)



class EventForm(Form):
    title = TextField('Title', [validators.Length(min=1, max=20)]) 
    #date = TextField('Date', [validators.Length(min=1, max=50)])
    date = DateField('Date', format='%d/%m/%Y', validators=(validators.Optional(),))
    location = TextField('Location', [validators.Length(min=1, max=100)])

def add_event_page():
    db = current_app.config["db"]
    form = EventForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        date = form.date.data
        location = form.location.data
        #event = Event(event_key, title, date, location)
        event_key = db.add_event(title, date, location)
        next_page = request.args.get("next", url_for("events_page"))    
        return redirect(next_page)
    return render_template("add_event.html", form=form, user_email=user_email, student_user=student_user, club_user=club_user)
    


#def eclub_page():
 #   db = current_app.config["db"]
  #  clubs = db.get_clubs()
   # return render_template("club.html", clubs = sorted(clubs))

def eclubs_page():
    db = current_app.config["db"]
    #club_key = 1
    club_key = request.args.get('club_key')
    club = db.get_club(club_key)
#    return redirect(url_for("a_club.html", club=club))
    return render_template("a_club.html", club=club, user_email=user_email, club_user=club_user, student_user=student_user)






def an_event_page():
    db = current_app.config["db"]
    event_key = request.args.get('event_key')
    form = CommentForm(request.form)
    comments =[]
    event = None
    if request.method == "POST" and form.validate():
        comment = form.comment.data
        name = form.name.data
        vote = form.vote.data
        db.add_comment(comment, name, vote, event_key)
        #event = db.get_event(event_key)
        #comments = db.get_comments()
    #club_key = 1
    if request.method == "GET":
        event = db.get_event(event_key)
        comments = db.get_comments(event_key)
    return render_template("an_event.html", event=event, comments=sorted(comments), user_email = user_email, club_user=club_user, student_user=student_user,form=form)
    




def account_page():
    db = current_app.config["db"]
    #club_key = 1
    email_user = request.args.get('user_email')
    user = None
    clubs = []
    events = []
    user_email = ""
    #email_user = user_email
    if email_user == "": 
        return render_template("account.html", user=user, user_email=user_email, club_user=club_user, student_user=student_user, clubs=clubs, events=events)
    if request.method == "GET" and email_user != "":
        if student_user:
            user = user_get(email_user)
            enrollments = db.get_enrollments(user.student_id)
            enrollments_events = db.get_enrollments_event(user.student_id)
            index = 0
            while index < len(enrollments):
                name = db.get_club(enrollments[index])
                clubs.append(name)
                index = index + 1
            index = 0
            while index < len(enrollments_events):
                events_name = db.get_event(enrollments_events[index])
                events.append(events_name)
                index = index+1
        if club_user: 
            user = user_get_club(email_user)  
        user_email = email_user
#    return redirect(url_for("a_club.html", club=club))
    return render_template("account.html", user=user, user_email = user_email, club_user=club_user, student_user=student_user, clubs=clubs, events=events)

def join_page():
    db = current_app.config["db"]
    #club_key = 1
    email_user = request.args.get('user_email')
    user = user_get(email_user)
    club_key = request.args.get('club_key')
    control = db.check_enrollment(user.student_id, club_key)
    if control > 0:
        flash("You already join to this club")
        return redirect(url_for("home_page"))
    if request.method == "GET":
        club = db.get_club(club_key)
        db.add_enrollment(user.student_id, club.club_id)
        db.update_number_members_club(club_key, club)
        updated_club = db.get_club(club_key)
#    return redirect(url_for("a_club.html", club=club))
    return render_template("join.html", club=updated_club, user_email = user_email, club_user=club_user, student_user=student_user)


def register_event_page():
    db = current_app.config["db"]
    #club_key = 1
    email_user = request.args.get('user_email')
    user = user_get(email_user)
    event_id = request.args.get('event_key')
    control = db.check_enrollment_event(user.student_id, event_id)
    if control == 1:
        flash("You are already registered")
#        return redirect(url_for("home_page"))
        return render_template("home.html", user_email=user_email, student_user=student_user, club_user=club_user )
    if request.method == "GET":
        db.add_enrollment_event(user.student_id, event_id)
        #event = db.get_event(event_id)
        #db.update_number_members_club(club_key, club)
        #updated_club = db.get_club(club_key)
#    return redirect(url_for("a_club.html", club=club))
    return render_template("home.html", user_email=user_email, student_user=student_user, club_user=club_user)
    #return render_template("an_event.html", event=event, user_email = user_email, club_user=club_user, student_user=student_user)

    
    
    


def eclub_page():
    db = current_app.config["db"]
    #db = Database(os.path.join(home_dir, "movies.sqlite"))
    #home_dir = os.path.expanduser("~")
    #db = Database(os.path.join(home_dir, "clubs.db"))
    #app.config["db"] = db
    if request.method == "GET":
        clubs = db.get_clubs()

        return render_template("club.html", clubs=sorted(clubs), user_email = user_email, club_user=club_user, student_user=student_user)
    else:
        if not current_user.is_admin():
            abort(401)
        form_club_keys = request.form.getlist("club_keys")
        for form_club_key in form_club_keys:
            db.delete_club(int(form_club_key))
        return redirect(url_for("eclub_page"))
    
def events_page():
    db = current_app.config["db"]
    #db = Database(os.path.join(home_dir, "movies.sqlite"))
    #home_dir = os.path.expanduser("~")
    #db = Database(os.path.join(home_dir, "clubs.db"))
    #app.config["db"] = db
    if request.method == "GET":
        events = db.get_events()
        return render_template("events.html", events=sorted(events), user_email = user_email,  club_user=club_user, student_user=student_user)
    else:
        form_event_keys = request.form.getlist("event_keys")
        for form_event_key in form_event_keys:
            db.delete_event(int(form_event_key))
        
        return render_template("events.html", events=sorted(events) , user_email = user_email,  club_user=club_user, student_user=student_user)
        #return redirect(url_for("event_page",user_available=user_available))

#@login_required
def club_add_page():
    if not current_user.is_admin:
        abort(401)
    if request.method == "GET":
        values = {"club_id":"" ,"name": "", "founder": "", "number_member":""}
        return render_template("club_edit.html",values = values)
    else:
        valid = validate_eclub_form(request.form)
        if not valid:
            return render_template(
                "club_edit.html")
        form_club_id = request.form["club_id"]
        form_name = request.form["name"]
        form_founder = request.form["founder"]
        form_number_member = request.form["number_member"]
        club = Club(form_club_id, form_name, form_founder, form_number_member)
        db = current_app.config["db"]
        club_key = db.add_club(club)
        return redirect(url_for("eclub_page", club_key=club_key, user_email=user_email,  club_user=club_user, student_user=student_user))
    
    
    

    
def validate_eclub_form(form):
    form.data = {}
    form.errors = {}

    form_name = form.get("name", "").strip()
    if len(form_name) == 0:
        form.errors["name"] = "Name can not be blank."
    else:
        form.data["name"] = form_name

    form_founder = form.get("founder", "").strip()
    if len(form_founder) == 0:
        form.errors["founder"] = "Founder can not be blank."
    else:
        form.data["founder"] = form_founder
    return len(form.errors) == 0



class LoginForm(Form): 

    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.Required()
    ])








def login_page():
    db = current_app.config["db"]

    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
            email = form.email.data                
            #user = User.query.get(email)
            user = is_user(email)
            #user = is_user(email)
            password = form.password.data
            if user is not None:
                if hasher.verify(password, user.password): 
                    login_user(user, remember = True)
                    flash("Log in is successfull")
                    #next_page = request.args.get("next", url_for("home_page"))
                   # print(current_user.is_admin)
                    global user_available
                    user_available = True
                    global user_email
                    user_email = user.email
                    global student_user
                    student_user = True 
                    #current_user.is_admin = True
                    return render_template("home.html", email=user.email, user_email = user_email, club_user=club_user, student_user=student_user)
                                           
            else: 
                flash("Wrong email or password.")
    return render_template("login.html", form=form)

def logout_page():
    logout_user()
    global student_user
    student_user = False
    global user_available 
    user_available = False
    global user_email
    user_email = ""
    flash("You have logged out.")
    return redirect(url_for("home_page"))

def login_clubs_page():
    db = current_app.config["db"]
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
            email = form.email.data                
            #user = User.query.get(email)
            user = get_user_club(email)
            #user = is_user(email)
            password = form.password.data
            if user is not None:
                if hasher.verify(password, user.password): 
                    login_user(user)
                    flash("Log in is successfull")
                    next_page = request.args.get("next", url_for("home_page"))
                    global user_available
                    user_available = True
                    global user_email
                    user_email = email
                    global club_user 
                    club_user = True
                    return render_template("home.html", user_email = user_email, club_user=club_user, student_user=student_user)
    #                   return redirect(next_page)
                else: 
                    flash("Wrong password or email.")
    return render_template("login_clubs.html", form=form)

def logout_club_page():
    logout_user()
    global user_email
    user_email = ""
    global user_available
    user_available = False
    global club_user
    club_user = False
    flash("You have logged out.")
    return redirect(url_for("home_page"))
    
#def login_page():
 #   form = LoginForm()
 #   if form.validate_on_submit():
 #       username = form.data["username"]
 #       user = get_user(username)
 #       if user is not None:

 #           password = form.data["password"]
 #           if hasher.verify(password, user.password):
 #               login_user(user)
  #              flash("You have logged in.")
  #              next_page = request.args.get("next", url_for("home_page"))
  #              return redirect(next_page)
  #      flash("Invalid credentials.")
  #  return render_template("login.html", form=form)

                    
                
#def login_page():
#    form = LoginForm()
 #   if form.validate_on_submit():
  #      email = form.data["email"]
   #     user = get_user(email)
    #    connection = psycopg2.connect(
#                  database="Database",
 #                 user="postgres",
  #                host="localhost",
   #               password="utku"
    #              )
#            cursor = connection.cursor()
 #           #cursor = psycopg2.connect("dbname=suppliers user=postgres password=postgres")
  #          cursor.execute(""" SELECT * FROM "STUDENT" WHERE (email = (%s)) AND (password = (%s))""",
   #                             (thwart(email), thwart(password)))
    #        email, password = cursor.fetchone()
     #   if user is not None:
#            password = form.data["password"]
 #           if hasher.verify(password, user.password):
  #              login_user(user)
   #             flash("You have logged in.")
    #            next_page = request.args.get("next", url_for("home_page"))
     #           return redirect(next_page)
#        flash("Invalid credentials.")
 #   return render_template("login.html", form=form)




class RegistrationFormClubs(Form):
    #username = TextField('Username', [validators.Length(min=4, max=20)])
    name = TextField('Name', [validators.Length(min=1, max=20)]) 
    founder = TextField('Founder', [validators.Length(min=1, max=50)])
    number_member = IntegerField('Number of Club Members', [validators.NumberRange(min=0, max=10000)])
    email = TextField('Email Adress', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required()
        #validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])
    
def register_club_page():
    db = current_app.config["db"]
    form = RegistrationFormClubs(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        founder = form.founder.data       
        number_member = form.number_member.data
        email = form.email.data
        #♥password = sha256_crypt.encrypt((str(form.password.data)))
        password = form.password.data
        student_id = 3
        test_email = db.is_register_available_club(email, name)
        if test_email is not None:
            flash("That email is already taken, please choose another")
            return render_template('signup_club.html', form=form)
        else:
            db.do_register_club(name, founder, number_member, email, password)
            flash("Thanks for registering!")
            next_page = request.args.get("next", url_for("home_page"))
            return redirect(next_page)
    return render_template("signup_club.html", form=form)





class RegistrationForm(Form):
    #username = TextField('Username', [validators.Length(min=4, max=20)])
    firstname = TextField('Username', [validators.Length(min=1, max=20)]) 
    surname = TextField('Surname', [validators.Length(min=1, max=50)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    department = TextField('Department', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required()
        #validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])
    
    
    
    
#@app.route('/register/', methods=["GET","POST"])
def register_page():
    db = current_app.config["db"]

    #try:
    form = RegistrationForm(request.form)

    if request.method == "POST" and form.validate():
        firstname = form.firstname.data
        surname = form.surname.data
        email = form.email.data
        department = form.department.data
        #password = sha256_crypt.encrypt((str(form.password.data)))
        password = form.password.data
        student_id = 3
        test_email = db.is_register_available(email, firstname)
        if test_email is not None:
            flash("That email is already taken, please choose another")
            return render_template('signup.html', form=form)

        else:
            db.do_register(firstname, surname, email, department, password)

            flash("Thanks for registering!")
            next_page = request.args.get("next", url_for("home_page"))
            return redirect(next_page)


    return render_template("signup.html", form=form)
