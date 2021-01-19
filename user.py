from flask import current_app
from flask_login import UserMixin
import sqlite3 as dbapi2
import psycopg2
from passlib.hash import pbkdf2_sha256 as hasher
import os

from flask import Flask, g, jsonify
from psycopg2 import pool

url = os.getenv("DATABASE_URL")


class Comment:
    def __init__(self, comment_id, comment, name, vote,event_id):
        self.comment_id = comment_id
        self.comment = comment
        self.name = name
        self.vote = vote
        self.event_id = event_id
    
    
    

class Event:
    def __init__(self, event_id, title, date, location):
        self.event_id = event_id
        self.title = title
        self.date = date
        self.location = location

class Account:
    def __init__(self, student_id, firstname, surname, email, department, password):
        self.student_id = student_id
        self.firstname = firstname
        self.surname = surname
        self.email = email
        self.department = department
        self.password = password
        
        
class AccountClub:
    def __init__(self, club_id, name, founder, number_member, email, password):
        self.club_id = club_id
        self.name = name
        self.founder = founder
        self.number_member = number_member 
        self.email = email
        self.password = password
        
        
class Enrollment:
    def __init__(self, student_id, club_id):
        self.student_id = student_id
        self.club_id = club_id

class User(UserMixin):
    def __init__(self, given_email, given_password):
        self.email = given_email
        self.password = given_password
        self.active = True
        self.is_admin = False

    def get_id(self):
        return self.email

    

    @property
    def is_active(self):
        return self.active
    



def user_get(student_email):
        
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    #cursor = psycopg2.connect("dbname=suppliers user=postgres password=postgres")
    query = """SELECT STUDENT_ID, FIRSTNAME, SURNAME, EMAIL, DEPARTMENT, PASSWORD FROM "STUDENT" WHERE (EMAIL = (%s))"""
    cursor.execute(query, (student_email,))
    student_id, firstname, surname, email, department, password = cursor.fetchone()
    user_ = Account(student_id, firstname, surname, email, department, password)
    return user_

def user_get_club(club_email):
        
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    #cursor = psycopg2.connect("dbname=suppliers user=postgres password=postgres")
    query = """SELECT CLUB_ID, NAME, FOUNDER, NUMBER_MEMBER, EMAIL, PASSWORD FROM "CLUBS" WHERE (EMAIL = (%s))"""
    cursor.execute(query, (club_email,))
    club_id, name, founder, number_member, email, password = cursor.fetchone()
    user_ = AccountClub(club_id, name, founder, number_member, email, password)
    return user_
    
def is_user(given_email):

    #with dbapi2.connect(dbfile) as connection:
        connection = psycopg2.connect(url)
        cursor = connection.cursor()
    #                query = """SELECT * FROM "STUDENT" WHERE (email= (%s)) AND (password = (%s))"""
              
        query = """SELECT PASSWORD FROM "STUDENT" WHERE (email= (%s))"""
        cursor.execute(query,(given_email,))
        password = cursor.fetchone()
        if password:
            new_password = hasher.hash(password[0])
            user = User(given_email, new_password) if password else None
            #password = current_app.config["PASSWORDS"].get(user.email)
             #current_app.config
            #user.password = password
            if user is not None: 
                user.is_admin = True
            #current_user.is_admin = True
            return user
                
        x = None
        return x 
    
def get_user(user_id):
        password = current_app.config["PASSWORDS"].get(user_id)
        user = User(user_id, password) if password else None
        if user is not None:
            user.is_admin = user.email in current_app.config["ADMIN_USERS"]
        return user
    
    
def update_user(self, user_key, student):
    with dbapi2.connect(self.dbfile) as connection:
        connection = psycopg2.connect(url)
        cursor = connection.cursor()
            #cursor = psycopg2.connect("dbname=suppliers user=postgres password=utku")
            
        query = """UPDATE "STUDENT" SET STUDENT_ID = (%s), FIRSTNAME = (%s), SURNAME = (%s) , EMAIL = (%s), DEPARTMENT = (%s)İ PASSWORD = (%S) WHERE (STUDENT_ID = (%s))"""
        cursor.execute(query, (student.student_id, student.firstname, student.surname, student.email, student.department, student.password ,user_key))
        connection.commit()
        
def delete_user(self, user_key):
        with dbapi2.connect(self.dbfile) as connection:
            connection = psycopg2.connect(url)
            cursor = connection.cursor()
            #cursor = psycopg2.connect("dbname=suppliers user=postgres password=utku")
            
            query = """DELETE FROM "STUDENT" WHERE (STUDENT_ID = (%s))"""
            cursor.execute(query, (user_key,))
            connection.commit()
    
def get_user_club(given_email):
        connection = psycopg2.connect(url)
        cursor = connection.cursor()              
        query = """SELECT PASSWORD FROM "CLUBS" WHERE (email= (%s))"""
        cursor.execute(query,(given_email,))
        password = cursor.fetchone()
        if password:
            new_password = hasher.hash(password[0])
            user = User(given_email, new_password) if password else None
            #user.password = password
            if user is not None: 
                user.is_admin = user.email 
            #current_user.is_admin = True
            return user
                
        x = None
        return x