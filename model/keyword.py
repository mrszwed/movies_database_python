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
from model.keywords_to_movies import keywords_to_movies_association_table
from model.movie import Movie
from model.person import Person
from model.credit import Credit


class Keyword(Base):
    __tablename__ = "keywords"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    movie_id = Column(Integer, ForeignKey("movies.tmdb_id"))
    movies = relationship("Movie", secondary=keywords_to_movies_association_table, back_populates="keywords")

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')

    def __repr__(self):
        return f"{self.id} {self.name}"

    @staticmethod
    def get_keywords(API_key, movie_id):
        query = 'https://api.themoviedb.org/3/movie/' + str(
            movie_id) + '/keywords' + '?api_key=' + API_key + '&language=en-US'
        response = requests.get(query)
        if response.status_code == 200:
            array = response.json()
            return [Keyword(**k) for k in array["keywords"]]
        else:
            return []


if __name__ == "__main__":
    print(Keyword.get_keywords(configuration.tmdb_API_key, 12))
