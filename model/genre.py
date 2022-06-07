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
from model.movies_to_genres import movies_to_genres_association_table


class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    movies = relationship("Movie", secondary=movies_to_genres_association_table, back_populates="genres")

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')

    def __repr__(self):
        return f"{self.id} {self.name}"

    @staticmethod
    def get_genre(API_key, genre_id):
        query = 'https://api.themoviedb.org/3/genre/' + str(genre_id) + '?api_key=' + API_key + '&language=en-US'
        response = requests.get(query)
        if response.status_code == 200:
            array = response.json()
            text = json.dumps(array)
            return Genre(**array)  # array - slownik, zwracany przez response
        else:
            return None


def get_and_save_genres():
    genres = []
    for i in range(30):
        m = Genre.get_genre(configuration.tmdb_API_key, i)
        if m is not None:
            genres.append(m)
            print(m)
    engine = sqlalchemy.create_engine(configuration.conn_string)
    with Session(engine) as session:
        session.add_all(genres)
        session.commit()


if __name__ == "__main__":
    get_and_save_genres()
