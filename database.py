import sqlite3 as dbapi2
from club import Club
import psycopg2
from user import User, Account, Enrollment, Event, Comment
from flask_login import current_user
from event import Event
import os

enrollment_key = 0
enrollment_event_key = 0
student_user_key = 0
club_user_key = 0
comment_key = 0
event_key = 0
url = os.getenv("DATABASE_URL")

class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile
        
    def add_enrollment(self, student_id, club_id):
        
        connection = psycopg2.connect(url)
        cursor = connection.cursor()
        global enrollment_key
        #enroll = Enrollment(student_id, club_id)
        enrollment_key = enrollment_key + 1
        #cursor = psycopg2.connect("dbname=suppliers user=postgres password=utku")
        query = """INSERT INTO "ENROLLMENT" (enrollment_id, student_id, club_id) VALUES ((%s), (%s), (%s))"""
        cursor.execute(query, (enrollment_key ,student_id, club_id))
        connection.commit()
        return enrollment_key 
        
    def get_enrollments(self, student_id):
       # with dbapi2.connect(self.dbfile) as connection:
        enrollments=[]
        connection = psycopg2.connect(url)
        cursor = connection.cursor()
        #cursor = psycopg2.connect("dbname=suppliers user=postgres password=postgres")
        query = """SELECT ENROLLMENT_ID, STUDENT_ID, CLUB_ID FROM "ENROLLMENT" WHERE (STUDENT_ID = (%s))"""
        cursor.execute(query, (student_id,))
        index = 0
        for enrollment_id, student_id, club_id in cursor:
            enrollments.append(club_id) 
        return enrollments




    def add_enrollment_event(self, student_id, event_id):
        connection = psycopg2.connect(url)
        cursor = connection.cursor()
        global enrollment_event_key
        #enroll = Enrollment(student_id, club_id)
        enrollment_event_key = enrollment_event_key + 1
        #cursor = psycopg2.connect("dbname=suppliers user=postgres password=utku")
        query = """INSERT INTO "ENROLLMENT_EVENT" (enrollment_event_id, student_id, event_id) VALUES ((%s), (%s), (%s))"""
        cursor.execute(query, (enrollment_event_key ,student_id, event_id))
        connection.commit()
        return enrollment_event_key 
    
    def check_enrollment_event(self, student_id, event_id):
        connection = psycopg2.connect(url)
        cursor = connection.cursor()
        query = """SELECT ENROLLMENT_EVENT_ID, STUDENT_ID, EVENT_ID FROM "ENROLLMENT_EVENT" WHERE (STUDENT_ID = (%s) AND EVENT_ID = (%s))"""
        cursor.execute(query, (student_id, event_id))
        enrollment_id = 0
        if cursor.fetchone() is not None:
            return 1
            #enrollment_id, student_id, event_id = cursor.fetchone()
        return 0
    
    def check_enrollment(self, student_id, club_id):
        connection = psycopg2.connect(url)
        cursor = connection.cursor()
        query = """SELECT ENROLLMENT_ID, STUDENT_ID, CLUB_ID FROM "ENROLLMENT" WHERE (STUDENT_ID = (%s) AND CLUB_ID = (%s))"""
        cursor.execute(query, (student_id, club_id))
        #enrollment_id = 0
        if cursor.fetchone() is not None:
            return 1
            #enrollment_id, student_id, event_id = cursor.fetchone()
        return 0

    
    def get_enrollments_event(self, student_id):
       # with dbapi2.connect(self.dbfile) as connection:
        enrollments_event=[]
        connection = psycopg2.connect(url)
        cursor = connection.cursor()
        #cursor = psycopg2.connect("dbname=suppliers user=postgres password=postgres")
        query = """SELECT ENROLLMENT_EVENT_ID, STUDENT_ID, EVENT_ID FROM "ENROLLMENT_EVENT" WHERE (STUDENT_ID = (%s))"""
        cursor.execute(query, (student_id,))
        index = 0
        for enrollment_event_id, student_id, event_id in cursor:
            enrollments_event.append(event_id) 
        return enrollments_event


    def add_comment(self, comment, name, vote, event_id):
        connection = psycopg2.connect(url)
        cursor = connection.cursor()
        global comment_key
        #enroll = Enrollment(student_id, club_id)
        comment_key = comment_key + 1
        #cursor = psycopg2.connect("dbname=suppliers user=postgres password=utku")
        query = """INSERT INTO "COMMENT" (comment, name, vote, event_id) VALUES ((%s), (%s), (%s), (%s))"""
        cursor.execute(query, (comment, name, vote, event_id))
        connection.commit()
        return comment_key 


    def get_comment(self, comment_key):
        connection = psycopg2.connect(url)
        cursor = connection.cursor()
        #cursor = psycopg2.connect("dbname=suppliers user=postgres password=postgres")
        query = """SELECT COMMENT_ID, COMMENT, NAME, VOTE, EVENT_ID FROM "COMMENT" WHERE (COMMENT_ID = (%s))"""
        cursor.execute(query, (comment_key,))
        comment_id, comment, name, vote, event_id = cursor.fetchone() 
        comment_ = Comment(comment_id, comment, name, vote, event_id)      
        return comment_


    def get_comments(self,event_key):
        comments = []
        #with dbapi2.connect(self.dbfile) as connection:
        connection = psycopg2.connect(url)
        cursor = connection.cursor()
        #cursor = psycopg2.connect("dbname=suppliers user=postgres password=utku")
        query = """SELECT COMMENT_ID, COMMENT, NAME, VOTE FROM "COMMENT" WHERE (EVENT_ID = (%s))"""
        cursor.execute(query, (event_key, ))
        comment_key = 1;
        for comment_id, comment, name, vote in cursor:
            comments.append((comment_key, Comment(comment_id, comment, name, vote, event_key)))
            comment_key = comment_key + 1
        return comments
    
    def update_comment(self, comment_key, comment):
        with dbapi2.connect(self.dbfile) as connection:
            connection = psycopg2.connect(url)
            cursor = connection.cursor()
            #cursor = psycopg2.connect("dbname=suppliers user=postgres password=utku")
            
            query = """UPDATE "COMMENT" SET COMMENT_ID = (%s), COMMENT = (%s), NAME = (%s) , VOTE = (%s), EVENT_ID = (%s) WHERE (COMMENT_ID = (%s))"""
            cursor.execute(query, (comment.comment_id, comment.comment, comment.name, comment.vote, comment.event_id,comment_key))
            connection.commit()
    
    def delete_comment(self, comment_key):
        with dbapi2.connect(self.dbfile) as connection:
            connection = psycopg2.connect(url)
            cursor = connection.cursor()
            #cursor = psycopg2.connect("dbname=suppliers user=postgres password=utku")
            
            query = """DELETE FROM "COMMENT" WHERE (COMMENT_ID = (%s))"""
            cursor.execute(query, (comment_key,))
            connection.commit()


    def add_event(self, title, date, location):
        with dbapi2.connect(self.dbfile) as connection:
            connection = psycopg2.connect(url)
            cursor = connection.cursor()
            global event_key 
            event_key = event_key + 1
            #cursor = psycopg2.connect("dbname=suppliers user=postgres password=utku")
            query = """INSERT INTO "EVENTS" (title, date, location) VALUES ((%s), (%s), (%s))"""
            cursor.execute(query, (event_key ,title, date, location))
            connection.commit()
            event_keys = cursor.lastrowid
        return event_keys
       
    def get_event(self, event_key):
       # with dbapi2.connect(self.dbfile) as connection:
        connection = psycopg2.connect(url)
        cursor = connection.cursor()
        #cursor = psycopg2.connect("dbname=suppliers user=postgres password=postgres")
        query = """SELECT EVENT_ID, TITLE, DATE, LOCATION FROM "EVENTS" WHERE (EVENT_ID = (%s))"""
        cursor.execute(query, (event_key,))
        event_id, title, date, location = cursor.fetchone() 
        event_ = Event(event_id, title, date, location)      
        return event_
    
    def get_events(self):
        events = []
        #with dbapi2.connect(self.dbfile) as connection:
        connection = psycopg2.connect(url)
        cursor = connection.cursor()
        #cursor = psycopg2.connect("dbname=suppliers user=postgres password=utku")
        query = """SELECT EVENT_ID, TITLE, DATE, LOCATION FROM "EVENTS" ORDER BY EVENT_ID"""
        cursor.execute(query)
        event_key = 1;
        for event_id, title, date, location in cursor:
            events.append((event_key, Event(event_id, title, date, location)))
            event_key = event_key + 1
        return events
    
    def update_event(self, event_key, event):
        with dbapi2.connect(self.dbfile) as connection:
            connection = psycopg2.connect(url)
            cursor = connection.cursor()
            #cursor = psycopg2.connect("dbname=suppliers user=postgres password=utku")
            
            query = """UPDATE "EVENTS" SET EVENT_ID = (%s), TITLE = (%s), DATE = (%s) , LOCATION = (%s) WHERE (EVENT_ID = (%s))"""
            cursor.execute(query, (event.event_id, event.title, event.date, event.location, event_key))
            connection.commit()
    
    def delete_event(self, event_key):
        with dbapi2.connect(self.dbfile) as connection:
            connection = psycopg2.connect(url)
            cursor = connection.cursor()
            #cursor = psycopg2.connect("dbname=suppliers user=postgres password=utku")
            
            query = """DELETE FROM "EVENTS" WHERE (EVENT_ID = (%s))"""
            cursor.execute(query, (event_key,))
            connection.commit()
            
            
    
    def add_club(self, club):
        with dbapi2.connect(self.dbfile) as connection:
            connection = psycopg2.connect(url)
            cursor = connection.cursor()
            #cursor = psycopg2.connect("dbname=suppliers user=postgres password=utku")
            query = """INSERT INTO "CLUBS" VALUES (club.name, club.founder, club.number_member, club.email, club.password)"""
            cursor.execute(query, (club.name, club.founder, club.number_member, club.email, club.password))
            connection.commit()
            club_key = cursor.lastrowid
        return club_key
    
    def update_club(self, club_key, club):
        with dbapi2.connect(self.dbfile) as connection:
            connection = psycopg2.connect(url)
            cursor = connection.cursor()
            #cursor = psycopg2.connect("dbname=suppliers user=postgres password=utku")
            
            query = """UPDATE "CLUBS" SET CLUB_ID = (%s), NAME = (%s), FOUNDER = (%s), NUMBER_MEMBER = (%s) , EMAIL = (%s), PASSWORD = (%s) WHERE (CLUB_ID = (%s))"""
            cursor.execute(query, (club.club_id, club.name, club.founder, club.number_member, club.email, club.password, club_key))
            connection.commit()
            
            
    def update_number_members_club(self, club_key, club):
        with dbapi2.connect(self.dbfile) as connection:
            connection = psycopg2.connect(url)
            cursor = connection.cursor()
            query = """SELECT NUMBER_MEMBER FROM "CLUBS" WHERE (CLUB_ID = (%s))"""
            cursor.execute(query, (club_key,))
            update_number = cursor.fetchone()
            updated_number = update_number[0] + 1   
            print(updated_number)
            query = """UPDATE "CLUBS" SET CLUB_ID =(%s), NAME = (%s), FOUNDER = (%s), NUMBER_MEMBER = (%s) , EMAIL = (%s), PASSWORD = (%s) WHERE (CLUB_ID = (%s))"""
            cursor.execute(query, (club.club_id, club.name, club.founder, updated_number, club.email, club.password, club_key))
            #club_id, name, founder, number_member, email, password = cursor.fetchone()
            #club_ = Club(club_id, name, founder, number_member, email, password)
            connection.commit()
        #return club_
    
    def delete_club(self, club_key):
        with dbapi2.connect(self.dbfile) as connection:
            connection = psycopg2.connect(url)
            cursor = connection.cursor()
            #cursor = psycopg2.connect("dbname=suppliers user=postgres password=utku")
            
            query = "DELETE FROM CLUBS WHERE (CLUB_ID = (%s))"
            cursor.execute(query, (club_key,))
            connection.commit()
            
    def get_club(self, club_key):
       # with dbapi2.connect(self.dbfile) as connection:
        connection = psycopg2.connect(url)
        cursor = connection.cursor()
        #cursor = psycopg2.connect("dbname=suppliers user=postgres password=postgres")
        query = """SELECT CLUB_ID, NAME, FOUNDER, NUMBER_MEMBER, EMAIL, PASSWORD, IMAGE FROM "CLUBS" WHERE (CLUB_ID = (%s))"""
        cursor.execute(query, (club_key,))
        club_id, name, founder, number_member, email, password, image = cursor.fetchone()
        club_ = Club(club_id, name, founder, number_member, email, password, image)
        return club_
    
    def get_clubs(self):
        clubs = []
        #with dbapi2.connect(self.dbfile) as connection:
        connection = psycopg2.connect(url)
        cursor = connection.cursor()
        #cursor = psycopg2.connect("dbname=suppliers user=postgres password=utku")
        query = """SELECT CLUB_ID, NAME, FOUNDER, NUMBER_MEMBER, EMAIL, PASSWORD FROM "CLUBS" ORDER BY CLUB_ID"""
        cursor.execute(query)
        image = "logo.png"
        club_key = 1;
        for club_id, name, founder, number_member, email, password in cursor:
            clubs.append((club_key, Club(club_id, name, founder, number_member, email, password, image)))
            club_key = club_key + 1
        return clubs
   
    
    def is_register_available_club(self, given_email, given_name):
         with dbapi2.connect(self.dbfile) as connection:
                connection = psycopg2.connect(url)
                cursor = connection.cursor()
                query = """SELECT EMAIL FROM "CLUBS" WHERE (email = (%s))"""
                cursor.execute(query, (given_email,))
                email = cursor.fetchone() 
         return email
    
    def do_register_club(self, name, founder, number_member, email, password):
         with dbapi2.connect(self.dbfile) as connection:
                connection = psycopg2.connect(url)
                cursor = connection.cursor()
                global club_user_key 
                club_user_key = club_user_key + 1 
                query = """INSERT INTO "CLUBS" (name, founder, number_member, email, password) VALUES ((%s), (%s), (%s), (%s), (%s))"""
                cursor.execute(query, (name, founder, number_member, email, password)) 
                connection.commit()
    
     
    
    def is_register_available(self, given_email, given_name):
         with dbapi2.connect(self.dbfile) as connection:
                connection = psycopg2.connect(url)
                cursor = connection.cursor()
                query = """SELECT EMAIL, FIRSTNAME FROM "STUDENT" WHERE (email = (%s)) AND (firstname = (%s))"""
                cursor.execute(query, (given_email, given_name))
                email = cursor.fetchone() 
         return email
     
    def do_register(self, firstname, surname, email, department, password):
         with dbapi2.connect(self.dbfile) as connection:
                connection = psycopg2.connect(url)
                cursor = connection.cursor()
                global student_user_key
                student_user_key = student_user_key + 1
                cursor.execute("""INSERT INTO "STUDENT" (firstname, surname, email, department, password) VALUES ((%s), (%s), (%s), (%s), (%s))""",
                    (firstname, surname, email, department, password)) 
                    #thwart("/introduction-to-python-programming/")
                connection.commit()
                #register_id = cursor.lastrowid
            #return register_id