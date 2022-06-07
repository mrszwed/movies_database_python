DROP TABLE IF EXISTS Movies;

CREATE TABLE Movies
(
	tmdb_id bigint PRIMARY KEY,
	imdb_id text,
	budget numeric,
	homepage text,
	original_language text,
	original_title text,
	overview text,
	imdb_popularity numeric,
	poster_path text,
	release_date date,
	revenue numeric,
	runtime bigint,
	status text,
	tagline text,
	title text,
	vote_average numeric,
	vote_count int
);

DROP TABLE IF EXISTS People;

CREATE TABLE People
(
	tmdb_id bigint PRIMARY KEY,
	imdb_id text,
	name text,
	place_of_birth text,
	popularity numeric,
	gender int,
	birthday date,
	deathday date,
	biography text,
	known_for_department text
);

ALTER TABLE people
ADD COLUMN profile_path text;

DROP TABLE IF EXISTS Credit_types;
CREATE TABLE Credit_types
(
	name text PRIMARY KEY
);


DROP TABLE IF EXISTS Credit_departments;
CREATE TABLE Credit_departments
(
	name text PRIMARY KEY
);

DROP TABLE IF EXISTS Credit_jobs;
CREATE TABLE Credit_jobs
(
	name text PRIMARY KEY
);

DROP TABLE IF EXISTS Credits;
CREATE TABLE Credits
(
	credit_id text PRIMARY KEY,
	people_id bigint,
	movie_id bigint ,
	credit_type_id text,
	credit_department_id text,
	credit_job_id text,
	CONSTRAINT fk_credits_movies
		FOREIGN KEY(movie_id) REFERENCES Movies(tmdb_id),
	CONSTRAINT fk_credits_people
		FOREIGN KEY(people_id) REFERENCES People(tmdb_id),	
	CONSTRAINT fk_credits_credit_types
		FOREIGN KEY(credit_type_id) REFERENCES Credit_types(name),
	CONSTRAINT fk_credits_credit_departments
		FOREIGN KEY(credit_department_id) REFERENCES Credit_departments(name),
	CONSTRAINT fk_credits_credit_jobs
		FOREIGN KEY(credit_job_id) REFERENCES Credit_jobs(name)
);

DROP TABLE IF EXISTS Genres;
CREATE TABLE Genres
(
	id bigint PRIMARY KEY,
	name text
);


DROP TABLE IF EXISTS Companies;
CREATE TABLE Companies
(
	tmdb_id bigint PRIMARY KEY,
	description text,
	headquarters text,
	homepage text,
	logo_path text,
	name text,
	origin_country text,
	parent_company bigint,
	CONSTRAINT fk_companies_companies
		FOREIGN KEY(parent_company) REFERENCES Companies(tmdb_id)
);

DROP TABLE IF EXISTS Countries;
CREATE TABLE Countries
(
	iso_3166_1 text PRIMARY KEY,
	name text
);

DROP TABLE IF EXISTS Named_entities;
CREATE TABLE Named_entities
(
	value text,
	tag text,
	PRIMARY KEY (value, tag)
);

DROP TABLE IF EXISTS Movies_to_named_entities;
CREATE TABLE Movies_to_named_entities
(
	named_entity_value text,
	named_entity_tag text,
	movie_id bigint,
	CONSTRAINT fk_named_entities_Movies_to_named_entities
		FOREIGN KEY (named_entity_value, named_entity_tag) REFERENCES named_entities(value, tag),
	CONSTRAINT fk_movies_Movies_to_named_entities
		FOREIGN KEY (movie_id) REFERENCES Movies(tmdb_id)
	
);

DROP TABLE IF EXISTS People_to_named_entities;
CREATE TABLE People_to_named_entities
(
	named_entity_value text,
	named_entity_tag text,
	people_id bigint,
	CONSTRAINT fk_named_entities_People_to_named_entities
		FOREIGN KEY (named_entity_value, named_entity_tag) REFERENCES named_entities(value, tag),
	CONSTRAINT fk_people_People_to_named_entities
		FOREIGN KEY (people_id) REFERENCES People(tmdb_id)
	
);


DROP TABLE IF EXISTS Movies_to_companies;
CREATE TABLE Movies_to_companies
(
	movie_id bigint,
	company_id bigint,
	CONSTRAINT fk_companies_Movies_to_companies
		FOREIGN KEY (company_id) REFERENCES Companies(tmdb_id),
	CONSTRAINT fk_movies_Movies_to_companies
		FOREIGN KEY (movie_id) REFERENCES Movies(tmdb_id)
	
);

DROP TABLE IF EXISTS Movies_to_genres;
CREATE TABLE Movies_to_genres
(
	movie_id bigint,
	genre_id bigint,
	CONSTRAINT fk_genres_Movies_to_genres
		FOREIGN KEY (genre_id) REFERENCES Genres(id),
	CONSTRAINT fk_movies_Movies_to_genres
		FOREIGN KEY (movie_id) REFERENCES Movies(tmdb_id)
);

DROP TABLE IF EXISTS Movies_to_countries;
CREATE TABLE Movies_to_countries
(
	movie_id bigint,
	iso_3166_1 text,
	CONSTRAINT fk_movies_Movies_to_countries
		FOREIGN KEY (movie_id) REFERENCES Movies(tmdb_id),
	CONSTRAINT fk_countries_Movies_to_countries
		FOREIGN KEY (iso_3166_1) REFERENCES Countries(iso_3166_1)
);

DROP TABLE IF EXISTS Reviews;
CREATE TABLE Reviews
(
	id text PRIMARY KEY,
	author text,
	content text,
	created_at date,
	movie_id bigint,
	CONSTRAINT fk_reviews_movies
		FOREIGN KEY (movie_id) REFERENCES Movies(tmdb_id)
);

DROP TABLE IF EXISTS Keywords;
CREATE TABLE Keywords
(
	id bigint PRIMARY KEY,
	name text
);

DROP TABLE IF EXISTS Keywords_to_movies;
CREATE TABLE Keywords_to_movies
(
	movie_id bigint,
	keyword_id bigint,
	CONSTRAINT fk_keywords_Keywords_to_movies
		FOREIGN KEY (keyword_id) REFERENCES Keywords(id),
	CONSTRAINT fk_movies_Keywords_to_movies
		FOREIGN KEY (movie_id) REFERENCES Movies(tmdb_id)
);


DROP TABLE IF EXISTS Reviews_to_named_entities;
CREATE TABLE Reviews_to_named_entities
(
	named_entity_value text,
	named_entity_tag text,
	review_id text,
	CONSTRAINT fk_named_entities_Reviews_to_named_entities
		FOREIGN KEY (named_entity_value, named_entity_tag) REFERENCES named_entities(value, tag),
	CONSTRAINT fk_reviews_Reviews_to_named_entities
		FOREIGN KEY (review_id) REFERENCES Reviews(id)
);

--indeksy

CREATE INDEX movies_title_idx ON Movies ((lower(title)));
CREATE INDEX movies_date_idx ON Movies (release_date);
CREATE INDEX named_entities_value_idx ON Named_entities ((lower(value)));
CREATE INDEX people_name_idx ON People ((lower(name)));
CREATE INDEX people_place_of_birth_idx ON People ((lower(place_of_birth)));
CREATE INDEX people_birthday_idx ON People (birthday);
CREATE INDEX genres_name_idx ON Genres ((lower(name)));
CREATE INDEX credits_people_id_idx ON Credits (people_id);
CREATE INDEX credits_movie_id_idx ON Credits (movie_id);
CREATE INDEX credits_credit_type_id_idx ON Credits (credit_type_id);
CREATE INDEX credits_credit_department_id_idx ON Credits (credit_department_id);
CREATE INDEX credits_credit_job_id_idx ON Credits (credit_job_id);
CREATE INDEX reviews_movie_id_idx ON Reviews (movie_id);


CREATE INDEX keywords_to_movies_movie_id_idx ON keywords_to_movies (movie_id);
CREATE INDEX keywords_to_movies_keyword_id_idx ON keywords_to_movies (keyword_id);
CREATE INDEX movies_to_companies_movie_id_idx ON movies_to_companies (movie_id);
CREATE INDEX movies_to_companies_company_id_idx ON movies_to_companies (company_id);
CREATE INDEX movies_to_countries_movie_id_idx ON movies_to_countries (movie_id);
CREATE INDEX movies_to_countries_iso_3166_1_idx ON movies_to_countries (iso_3166_1);
CREATE INDEX movies_to_genres_movie_id_idx ON movies_to_genres (movie_id);
CREATE INDEX movies_to_genres_genre_id_idx ON movies_to_genres (genre_id);
CREATE INDEX movies_to_named_entities_movie_id_idx ON movies_to_named_entities (movie_id);
CREATE INDEX people_to_named_entities_people_id_idx ON people_to_named_entities (people_id);
CREATE INDEX reviews_to_named_entities_review_id_idx ON reviews_to_named_entities (review_id);
