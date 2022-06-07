import requests
from sqlalchemy import Column, Numeric, Date
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from model.base import Base


class Person(Base):
    __tablename__ = "people"
    # __table_args__ = {'extend_existing': True}
    tmdb_id = Column(Integer, primary_key=True)
    imdb_id = Column(String)
    name = Column(String)
    place_of_birth = Column(String)
    profile_path = Column(String)
    popularity = Column(Numeric)
    gender = Column(Integer)
    birthday = Column(Date)
    deathday = Column(Date)
    biography = Column(String)
    known_for_department = Column(String)
    named_entities = relationship("NamedEntity", secondary='people_to_named_entities', back_populates="people")
    credits = relationship("Credit", back_populates="people")

    def __init__(self, **kwargs):  # slownik keywords argument
        self.tmdb_id = kwargs.get('id')
        self.imdb_id = kwargs.get('imdb_id')
        self.name = kwargs.get('name')
        self.place_of_birth = kwargs.get('place_of_birth')
        self.profile_path = kwargs.get('profile_path')
        self.popularity = kwargs.get('popularity')
        self.gender = kwargs.get('gender')
        if kwargs.get('birthday') == "":
            self.birthday = None
        else:
            self.birthday = kwargs.get('birthday')
        if kwargs.get('deathday') == "":
            self.deathday = None
        else:
            self.deathday = kwargs.get('deathday')
        self.biography = kwargs.get('biography')
        self.known_for_department = kwargs.get('known_for_department')

    def __repr__(self):
        return f"{self.tmdb_id} {self.name}  {self.place_of_birth} {self.popularity} {self.imdb_id}"

    @staticmethod
    def get_person(API_key, person_id):
        person_id = str(person_id)
        query = 'https://api.themoviedb.org/3/person/' + person_id + '?api_key=' + API_key + '&language=en-US'
        response = requests.get(query)
        if response.status_code == 200:
            array = response.json()  # slownik
            if array is None:
                return None
            p = Person(**array)
            # print(p)
            return p
        else:
            return None
