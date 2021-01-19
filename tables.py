from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Column, Table
from sqlalchemy import Float, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapper
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

uri = 'postgres://vagrant:vagrant@localhost:5432/itucsdb'
# engine = create_engine(uri, echo=True)
engine = create_engine(uri)

metadata = MetaData()

person_table = Table('Person', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('name', String(40)))

movie_table = Table('Movie', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('title', String(80), nullable=False),
                    Column('yr', Integer),
                    Column('score', Float),
                    Column('votes', Integer),
                    Column('directorid', Integer, ForeignKey('Person.id')))

casting_table = Table('Casting', metadata,
                      Column('movieid', Integer, ForeignKey('Movie.id'),
                             primary_key=True),
                      Column('actorid', Integer, ForeignKey('Person.id'),
                             primary_key=True),
                      Column('ord', Integer))