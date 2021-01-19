import os
import sys

import psycopg2 as dbapi2





INIT_STATEMENTS = [
    """CREATE TABLE CLUB (
        CLUB_ID SERIAL PRIMARY KEY,
        NAME VARCHAR(40) NOT NULL,     
        FOUNDER VARCHAR(40) NOT NULL,
        NUMBER_MEMBER INTEGER NOT NULL,
        EMAİL VARCHAR(70) NOT NULL,
        PASSWORD VARCHAR(200) NOT NULL,
        )""",
    """CREATE TABLE STUDENT (
        STUDENT_ID SERIAL PRIMARY KEY,
        FIRSTNAME VARCHAR(40) NOT NULL,     
        SURNAME VARCHAR(40) NOT NULL,
        EMAIL VARHCHAR(70) NOT NULL,
        DEPARTMNET VARCHAR(70) NOT NULL,
        PASSWORD VARCHAR(200) NOT NULL,
        )""",
    """CREATE TABLE EVENTS (
        EVENT_ID SERIAL PRIMARY KEY,
        TITLE VARCHAR(70) NOT NULL,     
        DATE TIMESTAP NOT NULL,
        LOCATION VARHCHAR(70) NOT NULL,
        )""",
    """CREATE TABLE COMMENT (
        COMMENT_ID SERIAL PRIMARY KEY,
        COMMENT VARCHAR(250) NOT NULL,     
        NAME VARCHAR(40) NOT NULL,
        VOTE INTEGER NOT NULL,
        EVENT_ID INTEGER NOT NULL,
        )""",
    """CREATE TABLE ENROLLMENT (
        ENROLLMENT_ID SERIAL PRIMARY KEY,
        STUDENT_ID INTEGER NOT NULL,
        CLUB_ID INTEGER NOT NULL,
        )""",
    """CREATE TABLE ENROLLMENT_EVENT (
        ENROLLMENT_EVENT_ID SERIAL PRIMARY KEY,
        STUDENT_ID INTEGER NOT NULL,
        CLUB_ID INTEGER NOT NULL,
        )""",    
    
    
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)