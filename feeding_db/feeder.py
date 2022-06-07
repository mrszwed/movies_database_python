import pandas as pd
import sqlalchemy

import configuration
from feeding_db.batch_generator import BatchGenerator
from feeding_db.extract_transform_load import get_and_save_companies, get_and_save_people, get_and_save_movies, \
    get_and_save_credits, get_and_save_reviews


def get_movie_ids(popularity_from):
    movie_data = pd.read_json("../resources/movie_ids_05_07_2022.json", lines=True)
    selection = movie_data[movie_data.popularity > popularity_from]
    ids = selection.id.to_numpy()
    print(movie_data.describe())
    ids = ids[ids != 665308]  # film z bledami, nie da sie przetworzyc
    return ids


def get_movies_by_popularity(cnt):
    movie_data = pd.read_json("../resources/movie_ids_05_07_2022.json", lines=True)
    movie_data_sorted = movie_data.sort_values(by=['popularity'], ascending=False)
    return movie_data_sorted.id[:cnt].to_numpy()


def get_person_ids(popularity_from):
    person_data = pd.read_json("../resources/person_ids_05_07_2022.json", lines=True)
    selection = person_data[person_data.popularity > popularity_from]
    # print(person_data.quantile(q=0.9))
    ids = selection.id.to_numpy()
    print(person_data.describe())
    return ids


def get_production_company_ids():
    pc_data = pd.read_json("../resources/production_company_ids_05_07_2022.json", lines=True)
    ids = pc_data.id.to_numpy()
    print(pc_data.describe())
    return ids


def get_company_ids_from_db():
    engine = sqlalchemy.create_engine(configuration.conn_string)
    df = pd.read_sql("SELECT tmdb_id FROM companies", engine)
    return df.tmdb_id.to_numpy()


def get_person_ids_from_db():
    engine = sqlalchemy.create_engine(configuration.conn_string)
    df = pd.read_sql("SELECT tmdb_id FROM people order by popularity DESC", engine)
    return df.tmdb_id.to_numpy()


# ------------------------------------------

def feed_db_with_companies():
    ids = get_company_ids_from_db()
    batch_gen = BatchGenerator(ids, batch_size=100)
    for batch in batch_gen:
        get_and_save_companies(batch, batch_gen, "feeder_companies.log")


def feed_db_with_people():
    ids = get_person_ids_from_db()
    batch_gen = BatchGenerator(ids, batch_size=100, start_from=145300)
    for batch in batch_gen:
        get_and_save_people(batch, batch_gen, "feeder_people_photo_update.log")


def feed_db_with_movies():
    ids = get_movies_by_popularity(30000)
    batch_gen = BatchGenerator(ids, batch_size=100, start_from=26200)
    for batch in batch_gen:
        get_and_save_movies(batch, batch_gen, "feeder_movies.log")


def get_db_movie_ids():
    engine = sqlalchemy.create_engine(configuration.conn_string)
    df = pd.read_sql("SELECT tmdb_id FROM movies", engine)
    return df.tmdb_id


def feed_db_with_credits():
    ids = get_db_movie_ids()
    batch_gen = BatchGenerator(ids, batch_size=100)
    for batch in batch_gen:
        get_and_save_credits(batch, batch_gen, "feeder_credits.log")
        print(f"batch {batch_gen.get_batch_number()}/{batch_gen.get_number_of_batches()}")


def feed_db_with_reviews():
    ids = get_db_movie_ids()
    batch_gen = BatchGenerator(ids, batch_size=100, start_from=10200)
    for batch in batch_gen:
        get_and_save_reviews(batch, batch_gen, "feeder_reviews.log")
        print(f"batch {batch_gen.get_batch_number()}/{batch_gen.get_number_of_batches()}")


if __name__ == "__main__":
    # feed_db_with_movies()
    # feed_db_with_credits()
    # feed_db_with_companies()
    # for k in get_db_movie_ids()[0:5]:
    #     print(k,type(k))
    # feed_db_with_reviews()
    feed_db_with_people()
