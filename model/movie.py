import json
import requests
import sqlalchemy
from sqlalchemy import Column, Numeric
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
import configuration
from feeding_db import ner_extraction
from model.base import Base
from model.company import Company
from model.country import Country
from model.genre import Genre
from model.keywords_to_movies import keywords_to_movies_association_table
from model.movies_to_companies import movies_to_companies_association_table
from model.movies_to_countries import movies_to_countries_association_table
from model.movies_to_genres import movies_to_genres_association_table


# from model.movies_to_named_entities import movies_to_named_entities_association_table, MoviesToNamedEntities


class Movie(Base):
    __tablename__ = "movies"
    # __table_args__ = {'extend_existing': True}
    tmdb_id = Column(Integer, primary_key=True)
    imdb_id = Column(String)
    budget = Column(Integer)
    homepage = Column(String)
    original_language = Column(String)
    original_title = Column(String)
    overview = Column(String)
    imdb_popularity = Column(Numeric)
    poster_path = Column(String)
    release_date = Column(String)
    revenue = Column(Integer)
    runtime = Column(Integer)
    status = Column(String)
    tagline = Column(String)
    title = Column(String)
    vote_average = Column(Numeric)
    vote_count = Column(Numeric)
    genres = relationship("Genre", secondary=movies_to_genres_association_table, back_populates="movies")
    countries = relationship("Country", secondary=movies_to_countries_association_table, back_populates="movies")
    companies = relationship("Company", secondary=movies_to_companies_association_table, back_populates="movies")
    named_entities = relationship("NamedEntity", secondary='movies_to_named_entities', back_populates="movies")
    credits = relationship("Credit", back_populates="movies")
    keywords = relationship("Keyword", secondary=keywords_to_movies_association_table, back_populates="movies")
    reviews = relationship("Review", back_populates="movies")

    def __init__(self, **kwargs):
        self.tmdb_id = kwargs.get('id')
        self.imdb_id = kwargs.get('imdb_id')
        self.budget = kwargs.get('budget')
        self.homepage = kwargs.get('homepage')
        self.original_language = kwargs.get('original_language')
        self.original_title = kwargs.get('original_title')
        self.overview = kwargs.get('overview')
        self.imdb_popularity = kwargs.get('imdb_popularity')
        self.poster_path = kwargs.get('poster_path')
        if kwargs.get('release_date') == "":
            self.release_date = None
        else:
            self.release_date = kwargs.get('release_date')
        self.revenue = kwargs.get('revenue')
        self.runtime = kwargs.get('runtime')
        self.status = kwargs.get('status')  # czy wydano
        self.tagline = kwargs.get('tagline')
        self.title = kwargs.get('title')
        self.vote_average = kwargs.get('vote_average')
        self.vote_count = kwargs.get('vote_count')
        # print(kwargs.get('genres'))
        genres = kwargs.get('genres')
        self.genres = []
        for i in genres:
            self.genres.append(Genre(**i))

        countries = kwargs.get('production_countries')
        self.countries = []
        for i in countries:
            self.countries.append(Country(**i))

        companies = kwargs.get('production_companies')
        self.companies = []
        for i in companies:
            self.companies.append(Company(**i))

    def __repr__(self):
        return f"{self.title} {self.release_date} revenue:{self.revenue} vote:{self.vote_average} genres:{self.genres}"

    @staticmethod
    def get_movie(API_key, movie_id):
        query = 'https://api.themoviedb.org/3/movie/' + str(movie_id) + '?api_key=' + API_key + '&language=en-US'
        response = requests.get(query)
        if response.status_code == 200:
            array = response.json()
            text = json.dumps(array)
            return Movie(**array)  # array - slownik, zwracany przez response
        else:
            return None


def get_movies():
    movies = []
    for i in range(30):
        m = Movie.get_movie(configuration.tmdb_API_key, i)
        if m is not None:
            movies.append(m)
            print(m)
