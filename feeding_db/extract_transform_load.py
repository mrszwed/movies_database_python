import traceback
import time
import requests
import sqlalchemy
from sqlalchemy import Column, Numeric, MetaData
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import Session
import configuration
from feeding_db import ner_extraction
from model.company import Company
from model.credit_type import CreditType
from model.movie import Movie
from model.person import Person
from model.credit import Credit
from model.keyword import Keyword
from model.reviews import Review
from model.base import Base
from sqlalchemy.sql import select


def get_and_save_companies(ids, batch_gen, log_file_name):
    companies = []
    with open(log_file_name, "a") as log_file:
        for i in ids:
            c = Company.get_company(configuration.tmdb_API_key, i)
            if c is not None:
                companies.append(c)
                print(c)
            else:
                print(f"{i} does not exist", file=log_file)

        engine = sqlalchemy.create_engine(configuration.conn_string)
        with Session(engine) as session:
            try:
                for c in companies:
                    session.merge(c)
                session.commit()
                current_time = time.strftime("%H:%M:%S", time.localtime())
                if batch_gen is not None:
                    print(
                        f"{current_time} Batch {batch_gen.get_batch_number()}/{batch_gen.get_number_of_batches()} has been processed.",
                        end=" ", file=log_file);
                print(f"Added: {[c.tmdb_id for c in companies]}", file=log_file)
            except Exception as e:
                print(traceback.format_exc(), file=log_file)


def get_and_save_movies(ids, batch_gen, log_file_name):
    movies = []
    with open(log_file_name, "a") as log_file:
        for i in ids:
            m = Movie.get_movie(configuration.tmdb_API_key, i)
            if m is not None:
                m.named_entities = ner_extraction.extract_NERs(m.overview)
                movies.append(m)
                print(m)
            else:
                print(f"{i} does not exist", file=log_file)
        engine = sqlalchemy.create_engine(configuration.conn_string)
        with Session(engine) as session:
            try:
                for m in movies:
                    session.merge(m)
                session.commit()
                current_time = time.strftime("%H:%M:%S", time.localtime())
                if batch_gen is not None:
                    print(
                        f"{current_time} Batch {batch_gen.get_batch_number()}/{batch_gen.get_number_of_batches()} has been processed.",
                        end=" ", file=log_file);
                print(f"Added: {[c.tmdb_id for c in movies]}", file=log_file)
            except Exception as e:
                print(traceback.format_exc(), file=log_file)


def get_and_save_people(ids, batch_gen, log_file_name):
    people = []
    with open(log_file_name, "a") as log_file:
        for i in ids:
            p = Person.get_person(configuration.tmdb_API_key, i)
            if p is not None:
                p.named_entities = ner_extraction.extract_NERs(p.biography)
                people.append(p)
                print(p)
            else:
                print(f"{i} does not exist", file=log_file)
        engine = sqlalchemy.create_engine(configuration.conn_string)
        with Session(engine) as session:
            try:
                for p in people:
                    session.merge(p)
                session.commit()
                current_time = time.strftime("%H:%M:%S", time.localtime())
                if batch_gen is not None:
                    print(
                        f"{current_time} Batch {batch_gen.get_batch_number()}/{batch_gen.get_number_of_batches()} has been processed.",
                        end=" ", file=log_file);
                print(f"Added: {[c.tmdb_id for c in people]}", file=log_file)
            except Exception as e:
                print(traceback.format_exc(), file=log_file)


def get_and_save_credits(ids, batch_gen, log_file_name):
    credits = []
    with open(log_file_name, "a") as log_file:
        for i in ids.astype(int):
            c = Credit.get_credits(configuration.tmdb_API_key, i)
            if c is not None:
                credits = credits + c
            else:
                print(f"{i} does not exist", file=log_file)
            # print(credits)
        engine = sqlalchemy.create_engine(configuration.conn_string)
        with Session(engine) as session:
            try:
                for c in credits:
                    session.merge(c)
                session.commit()
                current_time = time.strftime("%H:%M:%S", time.localtime())
                if batch_gen is not None:
                    print(
                        f"{current_time} Batch {batch_gen.get_batch_number()}/{batch_gen.get_number_of_batches()} has been processed.",
                        end=" ", file=log_file);
                print(f"Added: {len(credits)} credits", file=log_file)
            except Exception as e:
                print(traceback.format_exc(), file=log_file)


def get_and_save_reviews(ids, batch_gen, log_file_name):
    reviews = []
    with open(log_file_name, "a") as log_file:
        for i in ids:
            r = Review.get_reviews(configuration.tmdb_API_key, i)
            if r is not None:
                reviews = reviews + r
            else:
                print(f"{i} does not exist", file=log_file)
            # print(reviews)
        for r in reviews:
            r.named_entities = ner_extraction.extract_NERs(r.content)
        engine = sqlalchemy.create_engine(configuration.conn_string)
        with Session(engine) as session:
            try:
                for r in reviews:
                    session.merge(r)
                session.commit()
                current_time = time.strftime("%H:%M:%S", time.localtime())
                if batch_gen is not None:
                    print(
                        f"{current_time} Batch {batch_gen.get_batch_number()}/{batch_gen.get_number_of_batches()} has been processed.",
                        end=" ", file=log_file);
                print(f"Added: {len(reviews)} reviews", file=log_file)
            except Exception as e:
                print(traceback.format_exc(), file=log_file)


if __name__ == "__main__":
    # get_and_save_companies([1,2,3,4,5,6,7],None,"feeder_companies.log")
    # get_and_save_movies([1, 2, 3, 4, 5, 6, 7],None, "feeder_movies.log")
    # get_and_save_people([1, 2, 3, 4, 5, 6, 7],None, "feeder_people.log")
    # get_and_save_credits([1, 2, 3, 4, 5, 6, 7],None, "feeder_credits.log")
    get_and_save_reviews([1, 2, 3, 4, 5, 6, 7, 12], None, "feeder_reviews.log")
