from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

import configuration
from model.company import Company
from model.credit_type import CreditType
from model.genre import Genre
from model.movie import Movie
from model.movies_to_genres import movies_to_genres_association_table
from model.movies_to_named_entities import MoviesToNamedEntities
from model.named_entity import NamedEntity
from model.person import Person
from model.credit import Credit
from model.keyword import Keyword
from model.reviews import Review
from model.base import Base
import sqlalchemy
from sqlalchemy.sql import select


def select_movies_by_title(session, title, date_from=None, date_to=None, match_title=False):
    query = session.query(Movie)
    title = f'%{title.lower()}%'
    if match_title is True:
        query = query.filter(Movie.title.match(title))
    else:
        query = query.filter(sqlalchemy.func.lower(Movie.title).like(title))
    if date_from is not None:
        query = query.filter(Movie.release_date >= date_from)
    if (date_to is not None):
        query = query.filter(Movie.release_date <= date_to)
    result = query.order_by(Movie.vote_count.desc()).all()
    return result


def select_movie_by_id(session, tmdb_id):
    query = session.query(Movie)
    query = query.filter(Movie.tmdb_id == tmdb_id)
    print(query)
    result = query.all()
    return result


def select_movies_by_people_id(session, tmdb_id):
    query = session.query(Movie).join(Movie.credits).filter(Credit.people_id == tmdb_id)
    result = query.all()
    return result


def select_movies_by_actor_name(session, actor, date_from=None, date_to=None, match_actor=False):
    query = session.query(Movie, Person).join(Movie.credits).join(Credit.type).join(Credit.people)
    actor = f'%{actor.lower()}%'
    if match_actor is True:
        query = query.filter(Person.name.match(actor))
    else:
        query = query.filter(sqlalchemy.func.lower(Person.name).like(actor))
    query = query.filter(CreditType.name.match('cast'))
    if date_from is not None:
        query = query.filter(Movie.release_date >= date_from)
    if (date_to is not None):
        query = query.filter(Movie.release_date <= date_to)
    # print(query)
    result = query.order_by(Movie.vote_count.desc()).all()
    return result


def select_movies_by_actors_or(session, actors, date_from=None, date_to=None, limit=100):
    filters = []
    for e in actors:
        filters.append(sqlalchemy.func.lower(Person.name) == sqlalchemy.func.lower(e))

    sub_actors = session.query(Movie.tmdb_id).join(Movie.credits).join(Credit.people).filter(
        Credit.credit_type_id == 'cast')
    sub_actors = sub_actors.filter(or_(*filters))
    if date_from is not None:
        sub_actors = sub_actors.filter(Movie.release_date >= date_from)
    if (date_to is not None):
        sub_actors = sub_actors.filter(Movie.release_date <= date_to)
    query = session.query(Movie).where(Movie.tmdb_id.in_(sub_actors.subquery()))
    # print(query)
    return query.order_by(Movie.vote_count.desc()).limit(limit).all()


def select_movies_directed_by(session, directors, date_from=None, date_to=None, limit=100):
    filters = []
    for e in directors:
        filters.append(sqlalchemy.func.lower(Person.name) == sqlalchemy.func.lower(e))

    sub_actors = session.query(Movie.tmdb_id).join(Movie.credits).join(Credit.people).filter(
        Credit.credit_type_id == 'crew').filter(Credit.credit_job_id == 'Director')
    sub_actors = sub_actors.filter(or_(*filters))
    if date_from is not None:
        sub_actors = sub_actors.filter(Movie.release_date >= date_from)
    if (date_to is not None):
        sub_actors = sub_actors.filter(Movie.release_date <= date_to)
    query = session.query(Movie).where(Movie.tmdb_id.in_(sub_actors.subquery()))
    # print(query)
    return query.order_by(Movie.vote_count.desc()).limit(limit).all()


def select_movies_by_named_entities_description(session, entities):
    query = session.query(Movie).join(Movie.named_entities)
    filters = []
    for e in entities:
        filters.append(NamedEntity.value == e)
    query = query.order_by(Movie.vote_count.desc()).filter(or_(*filters))

    result = query.all()
    return result


def select_movies_by_named_entity_reviews(session, entities):
    query = session.query(Movie).join(Movie.reviews).join(Review.named_entities)
    filters = []
    for e in entities:
        filters.append(sqlalchemy.func.lower(NamedEntity.value) == sqlalchemy.func.lower(e))
    query = query.filter(or_(*filters))
    # print(query)
    result = query.order_by(Movie.vote_count.desc()).all()
    return result


def select_movies_by_named_entities(session, entities, limit=100):
    """

    :param session:
    :param entities:
    :return: zwraca liste filmow na podstawie znalezionych named entities w opisie filmu i review
    """
    filters = []
    for e in entities:
        filters.append(sqlalchemy.func.lower(NamedEntity.value) == sqlalchemy.func.lower(e))

    sub_description = session.query(Movie.tmdb_id).join(Movie.named_entities)
    sub_description = sub_description.filter(or_(*filters))
    sub_reviews = session.query(Movie.tmdb_id).join(Movie.reviews).join(Review.named_entities)
    sub_reviews = sub_reviews.filter(or_(*filters))

    union = sub_description.union(sub_reviews)
    query = session.query(Movie).where(Movie.tmdb_id.in_(union))
    return query.order_by(Movie.vote_count.desc()).limit(limit).all()


def select_movies_by_named_entities_or(session, entities, limit=100):
    filters = []
    for e in entities:
        filters.append(sqlalchemy.func.lower(NamedEntity.value) == sqlalchemy.func.lower(e))

    sub_description = session.query(Movie.tmdb_id).join(Movie.named_entities)
    sub_description = sub_description.filter(or_(*filters))

    query = session.query(Movie).where(Movie.tmdb_id.in_(sub_description.subquery()))
    return query.order_by(Movie.vote_count.desc()).limit(limit).all()


def select_movies_by_named_entities_and(session, entities):
    query = session.query(Movie)
    for e in entities:
        sub = session.query(MoviesToNamedEntities.movie_id).join(NamedEntity).filter(NamedEntity.value == e)
        subquery = sub.subquery()
        query = query.filter(Movie.tmdb_id.in_(subquery))
    result = query.order_by(Movie.vote_count.desc()).all()
    return result


def select_movies_by_two_actors(session, actors, date_from=None, date_to=None):
    query = session.query(Movie)
    for e in actors:
        e = f'%{e.lower()}%'
        sub = session.query(Credit.movie_id).join(Person).filter(sqlalchemy.func.lower(Person.name).like(e)).filter(
            Credit.credit_type_id == 'cast')
        subquery = sub.subquery()
        query = query.filter(Movie.tmdb_id.in_(subquery))
    if date_from is not None:
        query = query.filter(Movie.release_date >= date_from)
    if (date_to is not None):
        query = query.filter(Movie.release_date <= date_to)
    result = query.order_by(Movie.vote_count.desc()).all()
    return result


def not_used_select_movies_by_named_entities_and(session, entities):
    filters = []
    for e in entities:
        filters.append(sqlalchemy.func.lower(NamedEntity.value) == sqlalchemy.func.lower(e))

    sub_description = session.query(Movie.tmdb_id).join(Movie.named_entities)
    sub_description = sub_description.filter(and_(*filters))
    sub_reviews = session.query(Movie.tmdb_id).join(Movie.reviews).join(Review.named_entities)
    sub_reviews = sub_reviews.filter(and_(*filters))

    union = sub_description.union(sub_reviews)
    query = session.query(Movie).where(Movie.tmdb_id.in_(union))
    return query.order_by(Movie.vote_count.desc()).all()


def select_movies_by_genres_or(session, genres, limit=20):
    for g in genres:
        g = g.lower()
    query = session.query(Movie).join(Movie.genres)
    query = query.where(sqlalchemy.func.lower(Genre.name).in_(genres))
    query = query.order_by(Movie.vote_count.desc()).limit(limit)
    result = query.all()
    return result


def select_movies_by_genres_and(session, genres, limit=20):
    query = session.query(Movie)
    for g in genres:
        g = g.lower()
        sub = session.query(Movie.tmdb_id).join(Movie.genres).filter(sqlalchemy.func.lower(Genre.name) == g)
        subquery = sub.subquery()
        query = query.filter(Movie.tmdb_id.in_(subquery))
    query = query.order_by(Movie.vote_count.desc()).limit(limit)
    result = query.all()
    return result


def get_movie_details(session, id):
    movie = session.query(Movie).filter(Movie.tmdb_id == id).scalar()
    query = session.query(Credit, Person).join(Person.credits).filter(Credit.movie_id == id)
    query = query.filter(Credit.credit_department_id == None).order_by(Person.popularity.desc())
    cast = query.all()
    query = session.query(Credit, Person).join(Person.credits).filter(Credit.movie_id == id)
    query = query.filter(Credit.credit_department_id.isnot(None)).order_by(Person.popularity.desc())
    crew = query.all()
    return movie, cast, crew


if __name__ == "__main__":
    # get_movie_details(182)
    engine = sqlalchemy.create_engine(configuration.conn_string)
    with Session(engine) as session:
        #     # result=select_movies_by_title(session, 'Ram', date_from='1980-01-12', date_to='2012-11-11')
        #     # result=select_movies_by_actor_name(session, "Polanski")
        #     # result=select_movies_by_named_entities(session, ["nakatomi plaza", "jaws"])
        #     # result=select_movies_by_genres_and(session, ['horror', 'comedy'])
        #     result = select_movie_by_id(session, 8891)
        result = select_movies_directed_by(session, ['Sylvester Stallone', 'Roman Polanski'])
        for i, k in enumerate(result):
            print(i, k)
            # for j in k:
            #     print(j,k[j])
