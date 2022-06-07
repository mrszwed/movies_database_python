import json
import requests
import sqlalchemy
from sqlalchemy import Column, Numeric
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import Session
import configuration
from model.base import Base
from model.movies_to_countries import movies_to_countries_association_table
from model.movies_to_genres import movies_to_genres_association_table


class Country(Base):
    __tablename__ = "countries"
    iso_3166_1 = Column(String, primary_key=True)
    name = Column(String)
    movies = relationship("Movie", secondary=movies_to_countries_association_table, back_populates="countries")

    def __init__(self, **kwargs):
        self.iso_3166_1 = kwargs.get('iso_3166_1')
        self.name = kwargs.get('name')

    def __repr__(self):
        return f"{self.iso_3166_1} {self.name}"
