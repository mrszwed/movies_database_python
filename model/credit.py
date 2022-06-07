import json
import requests
import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import Session
import configuration
from model.base import Base
from model.credit_department import CreditDepartment
from model.credit_job import CreditJob
from model.company import Company
from model.movie import Movie
from model.person import Person
from model.credit_type import CreditType
from model.credit_job import CreditJob
from model.credit_department import CreditDepartment


class Credit(Base):
    __tablename__ = "credits"
    credit_id = Column(String, primary_key=True)
    people_id = Column(Integer, ForeignKey("people.tmdb_id"))
    people = relationship("Person", back_populates="credits")
    movie_id = Column(Integer, ForeignKey("movies.tmdb_id"))
    movies = relationship("Movie", back_populates="credits")
    credit_type_id = Column(String, ForeignKey("credit_types.name"))
    type = relationship("CreditType")
    credit_department_id = Column(String, ForeignKey("credit_departments.name"))
    department = relationship("CreditDepartment")
    credit_job_id = Column(String, ForeignKey("credit_jobs.name"))
    job = relationship("CreditJob")

    def __init__(self, movie_id, type, **kwargs):
        self.movie_id = movie_id
        self.type = CreditType(type)
        self.credit_id = kwargs.get("credit_id")
        department = kwargs.get("department")
        if department is None:
            self.department = None
        else:
            self.department = CreditDepartment(department)
        job = kwargs.get("job")
        if job is None:
            self.job = None
        else:
            self.job = CreditJob(job)
        p = Person(**kwargs)
        self.people = p
        self.people_id = p.tmdb_id

    def __repr__(self):
        return f"{self.movie_id} {self.type} people_id:{self.people_id} credit_id:{self.credit_id}, job:{self.job} department:{self.department}"

    @staticmethod
    def get_credits(API_key, movie_id):
        query = 'https://api.themoviedb.org/3/movie/' + str(
            movie_id) + '/credits' + '?api_key=' + API_key + '&language=en-US'
        response = requests.get(query)
        if response.status_code == 200:
            array = response.json()
            text = json.dumps(array)
            # print(text)
            # return Movie(**array)  # array - slownik, zwracany przez response
            credit_list = []
            for k in array:
                if k == "id":  # movie_id
                    continue
                credit_type = k
                for d in array[k]:
                    credit = Credit(movie_id, credit_type, **d)
                    # print(credit)
                    credit_list.append(credit)
            return credit_list
        else:
            return None

# Credit.get_credits(configuration.tmdb_API_key, 12)
