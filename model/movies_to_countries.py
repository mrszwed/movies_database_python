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

movies_to_countries_association_table = Table('movies_to_countries', Base.metadata,
                                              Column('movie_id', ForeignKey('movies.tmdb_id'), primary_key=True),
                                              Column('iso_3166_1', ForeignKey('countries.iso_3166_1'), primary_key=True)
                                              )
