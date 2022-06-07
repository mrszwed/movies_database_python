import requests
from sqlalchemy import Column, Numeric, Date, ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
import configuration
from model.base import Base
from model.movie import Movie
from model.person import Person
from model.credit import Credit
from model.keyword import Keyword
from model.reviews_to_named_entities import ReviewsToNamedEntities


class Review(Base):
    __tablename__ = "reviews"
    id = Column(String, primary_key=True)
    author = Column(String)
    content = Column(String)
    created_at = Column(Date)
    movie_id = Column(Integer, ForeignKey("movies.tmdb_id"))
    movies = relationship("Movie", back_populates="reviews")
    named_entities = relationship("NamedEntity", secondary='reviews_to_named_entities', back_populates="reviews")

    def __init__(self, movie_id, **kwargs):  # slownik keywords argument
        self.id = kwargs.get('id')
        self.author = kwargs.get('author')
        self.content = kwargs.get('content')
        if kwargs.get('created_at') == "":
            self.created_at = None
        else:
            self.created_at = kwargs.get('created_at')
        self.movie_id = movie_id

    def __repr__(self):
        return f"{self.id} {self.author}  {self.movie_id} {self.content} {self.created_at}"

    @staticmethod
    def get_reviews(API_key, movie_id):
        movie_id = str(movie_id)
        query = 'https://api.themoviedb.org/3/movie/' + movie_id + '/reviews' + '?api_key=' + API_key + '&language=en-US'
        response = requests.get(query)
        if response.status_code == 200:
            array = response.json()  # slownik
            return [Review(movie_id, **k) for k in array["results"]]
        else:
            return []


if __name__ == "__main__":
    print(Review.get_reviews(configuration.tmdb_API_key, 12))
