import json
import requests
import sqlalchemy
from sqlalchemy import Column, Table
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
import configuration
from model.base import Base

movies_to_genres_association_table = Table('movies_to_genres', Base.metadata,
                                           Column('movie_id', ForeignKey('movies.tmdb_id'), primary_key=True),
                                           Column('genre_id', ForeignKey('genres.id'), primary_key=True)
                                           )
