from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

import configuration
from model.company import Company
from model.credit_department import CreditDepartment
from model.credit_job import CreditJob
from model.credit_type import CreditType
from model.movie import Movie
from model.movies_to_named_entities import MoviesToNamedEntities
from model.named_entity import NamedEntity
from model.person import Person
from model.credit import Credit
from model.keyword import Keyword
from model.reviews import Review
from model.base import Base
import sqlalchemy
from sqlalchemy.sql import select


def select_people(session, name, place_of_birth=None, birthday=None, date_from=None, date_to=None, match_name=False):
    query = session.query(Person)
    if match_name is True:
        query = query.filter(Person.name == name)
    else:
        name = f'%{name.lower()}%'
        query = query.filter(sqlalchemy.func.lower(Person.name).like(name))
    if date_from is not None:
        query = query.filter(Person.birthday >= date_from)
    if (date_to is not None):
        query = query.filter(Person.birthday <= date_to)
    if (birthday is not None):
        query = query.filter(Person.birthday == birthday)
    if (place_of_birth is not None):
        place_of_birth = f'%{place_of_birth.lower()}%'
        query = query.filter(sqlalchemy.func.lower(Person.place_of_birth).like(place_of_birth))
    # print(query)
    result = query.order_by(Person.popularity.desc()).all()
    return result


def select_person_by_id(session, tmdb_id):
    query = session.query(Person)
    query = query.filter(Person.tmdb_id == tmdb_id)
    result = query.all()
    return result


def select_people_by_movie_id(session, tmdb_id):
    query = session.query(Person, Credit).join(Movie.credits).filter(Credit.movie_id == tmdb_id)
    result = query.all()
    return result


def select_actors_from_movie(session, title):
    query = session.query(Person, Movie.title).join(Person.credits).join(Credit.movies)
    title = f'%{title.lower()}%'
    query = query.filter(sqlalchemy.func.lower(Movie.title).like(title))
    query = query.filter(Credit.credit_type_id == 'cast')
    result = query.order_by(Person.popularity.desc()).all()
    return result


def select_crew_from_movie(session, title, jobs=None, department=None):
    query = session.query(Person, Credit, Movie).join(Person.credits).join(Credit.movies)
    query = query.filter(Credit.credit_department_id.isnot(None))

    title = f'%{title.lower()}%'
    query = query.filter(sqlalchemy.func.lower(Movie.title).like(title))
    if jobs is not None:
        query = query.join(Credit.job)
        for j in jobs:
            j = f'%{j.lower()}%'
            query = query.filter(sqlalchemy.func.lower(CreditJob.name).like(j))
    if department is not None:
        query = query.join(Credit.department)
        department = f'%{department.lower()}%'
        query = query.filter(sqlalchemy.func.lower(CreditDepartment.name).like(department))

    result = query.order_by(Person.popularity.desc()).all()
    return result


def get_person_details(session, id):
    person = session.query(Person).filter(Person.tmdb_id == id).scalar()
    query = session.query(Credit, Movie).join(Movie.credits).filter(Credit.people_id == id)
    query = query.filter(Credit.credit_department_id == None).order_by(Movie.vote_count.desc())
    person_movies = query.all()
    return person, person_movies


def select_credits(session, person_id, movie_id):
    query = session.query(Credit).filter(Credit.people_id == person_id).filter(Credit.movie_id == movie_id)
    result = query.all()
    return result


def get_credits(person_id, movie_id):
    engine = sqlalchemy.create_engine(configuration.conn_string)
    with Session(engine) as session:
        result = select_credits(session=session, person_id=person_id, movie_id=movie_id)
    return result


def list_crew(title):
    engine = sqlalchemy.create_engine(configuration.conn_string)
    with Session(engine) as session:
        result = select_crew_from_movie(session, title="Die Hard")
        for i, k in enumerate(result):
            print(i, k)


if __name__ == "__main__":
    list_crew('Die Hard')
    # engine = sqlalchemy.create_engine(configuration.conn_string)
    # with Session(engine) as session:
    #     # result=select_people(session, name="john", place_of_birth='los angeles', date_from='1990-01-01', match_name=False)
    #     # for i,k in enumerate(result):
    #     #     print(i,k)
    #
    #     result = select_crew_from_movie(session, title="Die Hard")
    #     # for i, k in enumerate(result):
    #     #     print(i, k)
    #
    #     # result = select_crew_from_movie(session, title="Die Hard", jobs=['Producer'])
    #     for i, k in enumerate(result):
    #         print(i, k)
    #         # print(k.title)
