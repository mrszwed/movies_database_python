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

keywords_to_movies_association_table = Table('keywords_to_movies', Base.metadata,
                                             Column('movie_id', ForeignKey('movies.tmdb_id'), primary_key=True),
                                             Column('keyword_id', ForeignKey('keywords.id'), primary_key=True)
                                             )
