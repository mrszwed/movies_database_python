import sqlalchemy
from dash import Dash, html, dcc, Input, Output, State, callback
from sqlalchemy.orm import Session

import configuration
from queries.query_movies import select_movie_by_id, select_movies_by_people_id, get_movie_details
from queries.query_people import select_credits, select_person_by_id, select_people_by_movie_id, get_person_details
from web.pages.menu_bar import menu_bar


def to_web_list(movies):
    children = []
    for m in movies:
        new_item = html.Li(m.tmdb_id)
        url = ""
        if m.poster_path is not None:
            url = f'https://www.themoviedb.org/t/p/w440_and_h660_face/' + m.poster_path
        new_item.children = [
            html.Div([
                html.Img(src=url, alt='foto', style={'height': '10%', 'width': '10%'}),
                html.Div([
                    # html.Span(m.title, style={'font-weight': 'bold', 'size': 50, 'margin':5}),
                    # dcc.Link('Movies by title', href='/movies_title', style={'margin': 10}),
                    dcc.Link(m.title, href='/movie/' + str(m.tmdb_id),
                             style={'font-weight': 'bold', 'size': 50, 'margin': 5}),
                    html.Span(m.release_date, style={'font-weight': 'normal', 'size': 12, 'margin': 5}),
                    html.Span(m.overview, style={'font-weight': 'normal', 'size': 12, 'margin': 5}),
                ],
                    style={"display": "flex", "flex-direction": "column"}
                )],
                style={"display": "flex", "flex-direction": "row", 'margin': 10, "background": "gainsboro"}
            ),
        ]
        children.append(new_item)
    return children


def to_web_list_with_actors(movies):
    children = []
    for m in movies:
        new_item = html.Li(m.Movie.tmdb_id)
        url = ""
        if m.Movie.poster_path is not None:
            url = f'https://www.themoviedb.org/t/p/w440_and_h660_face/' + m.Movie.poster_path
        new_item.children = [
            html.Div([
                html.Img(src=url, alt='foto', style={'height': '10%', 'width': '10%'}),
                html.Div([
                    dcc.Link(m.Movie.title, href='/movie/' + str(m.Movie.tmdb_id),
                             style={'font-weight': 'bold', 'size': 50, 'margin': 5}),
                    # html.Span(m.Movie.title, style={'font-weight': 'bold', 'size': 50, 'margin':5}),
                    html.Span(m.Movie.release_date, style={'font-weight': 'normal', 'size': 12, 'margin': 5}),
                    html.Span(m.Movie.overview, style={'font-weight': 'normal', 'size': 12, 'margin': 5}),
                    html.Span(m.Person.name, style={'font-style': 'italic', 'size': 12, 'margin': 5}),
                ],
                    style={"display": "flex", "flex-direction": "column"}
                )],
                style={"display": "flex", "flex-direction": "row", 'margin': 10, "background": "gainsboro"}
            ),
        ]
        children.append(new_item)
    return children


def to_web_list_with_genres(movies):
    children = []
    for m in movies:
        new_item = html.Li(m.tmdb_id)
        url = ""
        if m.poster_path is not None:
            url = f'https://www.themoviedb.org/t/p/w440_and_h660_face/' + m.poster_path
        genres_list = []
        for g in m.genres:
            genres_list.append(html.Span(g.name, style={'font-style': 'italic', 'size': 12, 'margin': 5}), )
        new_item.children = [
            html.Div([
                html.Img(src=url, alt='foto', style={'height': '10%', 'width': '10%'}),
                html.Div([
                    dcc.Link(m.title, href='/movie/' + str(m.tmdb_id),
                             style={'font-weight': 'bold', 'size': 50, 'margin': 5}),
                    # html.Span(m.title, style={'font-weight': 'bold', 'size': 50, 'margin':5}),
                    html.Span(m.release_date, style={'font-weight': 'normal', 'size': 12, 'margin': 5}),
                    html.Span(m.overview, style={'font-weight': 'normal', 'size': 12, 'margin': 5}),
                    html.Div(genres_list, style={'font-weight': 'normal', 'size': 12, 'margin': 5})
                    # html.Span(m.genres, style={'font-style': 'italic', 'size': 12, 'margin': 5}),
                ],
                    style={"display": "flex", "flex-direction": "column"}
                )],
                style={"display": "flex", "flex-direction": "row", 'margin': 10, "background": "gainsboro"}
            ),
        ]
        children.append(new_item)
    return children


def to_web_list_with_named_entities(movies, named_entities=None):
    children = []
    if named_entities is not None:
        ners = [html.Span(e[0] + ' | ' + e[1],
                          style={'background': '#73AD21', 'border-radius': '5px', 'padding': 7, 'margin': 5}) for e in
                named_entities]
        ners.insert(0, html.Span('Extracted:', style={'font-weight': 'bold'}))
        children.append(html.Div(ners))
    for m in movies:
        new_item = html.Li(m.tmdb_id)
        url = ""
        if m.poster_path is not None:
            url = f'https://www.themoviedb.org/t/p/w440_and_h660_face/' + m.poster_path
        named_entities_list = []
        for g in m.named_entities:
            named_entities_list.append(html.Span(g.value + ' | ' + g.tag,
                                                 style={'background': '#73AD21', 'border-radius': '5px', 'padding': 7,
                                                        'margin': 2}))
            # named_entities_list.append(html.Span('['+g.value+' | '+g.tag+']', style={'font-style': 'italic', 'size': 12, 'margin': 5}),)
        new_item.children = [
            html.Div([
                html.Img(src=url, alt='foto', style={'height': '10%', 'width': '10%'}),
                html.Div([
                    dcc.Link(m.title, href='/movie/' + str(m.tmdb_id),
                             style={'font-weight': 'bold', 'size': 50, 'margin': 5}),
                    # html.Span(m.title, style={'font-weight': 'bold', 'size': 50, 'margin':5}),
                    html.Span(m.release_date, style={'font-weight': 'normal', 'size': 12, 'margin': 5}),
                    html.Span(m.overview, style={'font-weight': 'normal', 'size': 12, 'margin': 5}),
                    html.Div(named_entities_list,
                             style={'font-weight': 'normal', 'size': 12, 'margin': 5, 'display': 'flex',
                                    'flex-flow': 'row wrap'})
                    # html.Span(m.genres, style={'font-style': 'italic', 'size': 12, 'margin': 5}),
                ],
                    style={"display": "flex", "flex-direction": "column"}
                )],
                style={"display": "flex", "flex-direction": "row", 'margin': 10, "background": "gainsboro"}
            ),
        ]
        children.append(new_item)
    return children


def to_web_list_people(people):
    children = []
    for m in people:
        new_item = html.Li(m.tmdb_id)
        url = "https://aui.atlassian.com/aui/8.8/docs/images/avatar-person.svg"
        if m.profile_path is not None:
            url = f'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/' + m.profile_path
        place_of_birth = "no information"
        if m.place_of_birth is not None:
            place_of_birth = m.place_of_birth
        birthday = "no information"
        if m.birthday is not None:
            birthday = str(m.birthday)
        biography = "no information"
        if m.biography is not None:
            biography = m.biography
        new_item.children = [
            html.Div([
                html.Img(src=url, alt='foto', style={'height': '10%', 'width': '10%'}),
                html.Div([
                    dcc.Link(m.name, href='/person/' + str(m.tmdb_id),
                             style={'font-weight': 'bold', 'size': 50, 'margin': 5}),
                    # html.Span(m.name, style={'font-weight': 'bold', 'size': 50, 'margin':5}),
                    html.Span('Place of birth: ' + place_of_birth,
                              style={'font-weight': 'normal', 'size': 12, 'margin': 5}),
                    html.Span('Birthday: ' + birthday, style={'font-weight': 'normal', 'size': 12, 'margin': 5}),
                    html.Span('Biography: ' + biography, style={'font-weight': 'normal', 'size': 12, 'margin': 5}),
                ],
                    style={"display": "flex", "flex-direction": "column"}
                )],
                style={"display": "flex", "flex-direction": "row", 'margin': 10, "background": "gainsboro"}
            ),
        ]
        children.append(new_item)
    return children


def to_web_list_actors(people):
    children = []
    for m in people:
        new_item = html.Li(m.Person.tmdb_id)
        url = "https://aui.atlassian.com/aui/8.8/docs/images/avatar-person.svg"
        if m.Person.profile_path is not None:
            url = f'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/' + m.Person.profile_path
        place_of_birth = "no information"
        if m.Person.place_of_birth is not None:
            place_of_birth = m.Person.place_of_birth
        birthday = "no information"
        if m.Person.birthday is not None:
            birthday = str(m.Person.birthday)
        biography = "no information"
        if m.Person.biography is not None:
            biography = m.Person.biography
        new_item.children = [
            html.Div([
                html.Img(src=url, alt='foto', style={'height': '10%', 'width': '10%'}),
                html.Div([
                    dcc.Link(m.Person.name, href='/person/' + str(m.Person.tmdb_id),
                             style={'font-weight': 'bold', 'size': 50, 'margin': 5}),
                    # html.Span(m.Person.name, style={'font-weight': 'bold', 'size': 50, 'margin':5}),
                    html.Span('Played in: ' + m.title, style={'font-style': 'italic', 'size': 16, 'margin': 8}),
                    html.Span('Place of birth: ' + place_of_birth,
                              style={'font-weight': 'normal', 'size': 12, 'margin': 5}),
                    html.Span('Birthday: ' + birthday, style={'font-weight': 'normal', 'size': 12, 'margin': 5}),
                    html.Span('Biography: ' + biography, style={'font-weight': 'normal', 'size': 12, 'margin': 5}),
                ],
                    style={"display": "flex", "flex-direction": "column"}
                )],
                style={"display": "flex", "flex-direction": "row", 'margin': 10, "background": "gainsboro"}
            ),
        ]
        children.append(new_item)
    return children


def to_web_list_crew(people):
    children = []
    for m in people:
        if m.Credit.credit_department_id is None:
            continue
        new_item = html.Li(m.Person.tmdb_id)
        url = "https://aui.atlassian.com/aui/8.8/docs/images/avatar-person.svg"
        if m.Person.profile_path is not None:
            url = f'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/' + m.Person.profile_path
        place_of_birth = "no information"
        if m.Person.place_of_birth is not None:
            place_of_birth = m.Person.place_of_birth
        birthday = "no information"
        if m.Person.birthday is not None:
            birthday = str(m.Person.birthday)
        biography = "no information"
        if m.Person.biography is not None:
            biography = m.Person.biography

        # credits=get_credits(m.Person.tmdb_id, m.Movie.tmdb_id)
        credits = []
        p_jobs = [html.Span('Job: ', style={'font-style': 'italic', 'size': 12, 'margin': 5})]
        p_departments = [html.Span('Department: ', style={'font-style': 'italic', 'size': 12, 'margin': 5})]
        p_jobs.append(html.Span(m.Credit.credit_job_id, style={'font-style': 'italic', 'size': 12, 'margin': 5}), )
        p_departments.append(
            html.Span(m.Credit.credit_department_id, style={'font-style': 'italic', 'size': 12, 'margin': 5}), )

        new_item.children = [
            html.Div([
                html.Img(src=url, alt='foto', style={'height': '10%', 'width': '10%'}),
                html.Div([
                    dcc.Link(m.Person.name, href='/person/' + str(m.Person.tmdb_id),
                             style={'font-weight': 'bold', 'size': 50, 'margin': 5}),
                    # html.Span(m.Person.name, style={'font-weight': 'bold', 'size': 50, 'margin':5}),
                    html.Span('Crew in: ' + m.Movie.title, style={'font-style': 'italic', 'size': 16, 'margin': 8}),
                    html.Div(p_departments, style={'font-weight': 'normal', 'size': 12, 'margin': 5}),
                    html.Div(p_jobs, style={'font-weight': 'normal', 'size': 12, 'margin': 5}),
                    html.Span('Place of birth: ' + place_of_birth,
                              style={'font-weight': 'normal', 'size': 12, 'margin': 5}),
                    html.Span('Birthday: ' + birthday, style={'font-weight': 'normal', 'size': 12, 'margin': 5}),
                    html.Span('Biography: ' + biography, style={'font-weight': 'normal', 'size': 12, 'margin': 5}),
                ],
                    style={"display": "flex", "flex-direction": "column"}
                )],
                style={"display": "flex", "flex-direction": "row", 'margin': 10, "background": "gainsboro"}
            ),
        ]
        children.append(new_item)
    return children


def to_web_list_movie_details(id):
    engine = sqlalchemy.create_engine(configuration.conn_string)
    with Session(engine) as session:
        m, cast, crew = get_movie_details(session, id)
        new_item = html.Li(m.tmdb_id, style={'list-style-type': 'none'})
        url = ""
        if m.poster_path is not None:
            url = f'https://www.themoviedb.org/t/p/w440_and_h660_face/' + m.poster_path
        release_date = 'no information'
        if m.release_date is not None:
            release_date = m.release_date
        budget = 'no information'
        if m.budget is not None or m.budget != 0:
            budget = m.budget
        homepage = 'no information'
        if m.homepage is not None:
            homepage = m.homepage
        original_language = 'no information'
        if m.original_language is not None:
            original_language = m.original_language
        status = 'no information'
        if m.status is not None:
            status = m.status
        runtime = 'no information'
        if m.runtime is not None or m.runtime != 0:
            runtime = m.runtime
        revenue = 'no information'
        if m.revenue is not None:
            revenue = m.revenue
        tagline = 'no information'
        if m.tagline is not None:
            tagline = m.tagline
        vote_average = 'no information'
        vote_count = '0'
        if m.vote_count != 0:
            vote_average = m.vote_average
            vote_count = m.vote_count

        cast_list = []
        for ca in cast:
            cast_list.append(html.Li(ca.Person.name, style={'font-style': 'italic', 'size': 9, 'margin': 3}))
        crew_list = []
        for cr in crew:
            crew_list.append(html.Li(cr.Person.name, style={'font-style': 'italic', 'size': 9, 'margin': 3}))
        new_item.children = [
            menu_bar(add_root=True),
            html.Div([
                html.Img(src=url, alt='foto', style={'height': '40%', 'width': '40%'}),
                html.Div([
                    html.Span(m.title, style={'font-weight': 'bold', 'size': 50, 'margin': 5}),
                    html.Span('Release date: ' + str(release_date),
                              style={'font-style': 'italic', 'size': 12, 'margin': 5}),
                    html.Span(m.overview, style={'font-weight': 'normal', 'size': 16, 'margin': 5}),
                    html.Span('Tagline: ' + tagline, style={'font-weight': 'normal', 'size': 12, 'margin': 5}),
                    html.Span('Homepage: ' + homepage, style={'font-style': 'italic', 'size': 9, 'margin': 3}),
                    html.Span('Runtime: ' + str(runtime), style={'font-style': 'italic', 'size': 9, 'margin': 3}),
                    html.Span('Budget: ' + str(budget), style={'font-style': 'italic', 'size': 9, 'margin': 3}),
                    html.Span('Revenue: ' + str(revenue), style={'font-style': 'italic', 'size': 9, 'margin': 3}),
                    html.Span('Original language: ' + original_language,
                              style={'font-style': 'italic', 'size': 9, 'margin': 3}),
                    html.Span('Status: ' + status, style={'font-style': 'italic', 'size': 9, 'margin': 3}),
                    html.Span('Vote average: ' + str(vote_average),
                              style={'font-style': 'italic', 'size': 9, 'margin': 3}),
                    html.Span('Vote count: ' + str(vote_count),
                              style={'font-style': 'italic', 'size': 9, 'margin': 3}),
                    html.Div([
                        html.Span('Cast:', style={'font-weight': 'bold', 'size': 9, 'margin': 3}),
                        html.Ul(cast_list, style={'font-style': 'normal', 'size': 9, 'margin': 3})
                    ]),
                    html.Div([
                        html.Span('Crew:', style={'font-weight': 'bold', 'size': 9, 'margin': 3}),
                        html.Ul(crew_list, style={'font-style': 'normal', 'size': 9, 'margin': 3})
                    ]),
                ],
                    style={"display": "flex", "flex-direction": "column"}
                )],
                style={"display": "flex", "flex-direction": "row", 'margin': 10, "background": "gainsboro"}
            ),
        ]
        # children.append(new_item)
        return new_item


def to_web_list_person_details(id):
    engine = sqlalchemy.create_engine(configuration.conn_string)
    with Session(engine) as session:
        m, movies = get_person_details(session, id)

        new_item = html.Li(m.tmdb_id, style={'list-style-type': 'none'})
        url = "https://aui.atlassian.com/aui/8.8/docs/images/avatar-person.svg"
        if m.profile_path is not None:
            url = f'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/' + m.profile_path
        place_of_birth = 'no information'
        if m.place_of_birth is not None:
            place_of_birth = m.place_of_birth
        popularity = 'no information'
        if m.popularity is not None:
            popularity = str(m.popularity)
        gender = 'no information'
        if m.gender is not None:
            if m.gender == 1:
                gender = 'woman'
            else:
                gender = 'man'
        birthday = 'no information'
        if m.birthday is not None:
            birthday = str(m.birthday)
        biography = 'no information'
        if m.biography is not None:
            biography = m.biography
        known_for_department = 'no information'
        if m.known_for_department is not None:
            known_for_department = m.known_for_department
        movies_list = []
        for mov in movies:
            movies_list.append(html.Li(mov.Movie.title + ' (' + str(mov.Movie.release_date.year) + ')',
                                       style={'font-style': 'italic', 'size': 9, 'margin': 3}))
        new_item.children = [
            menu_bar(add_root=True),
            html.Div([
                html.Img(src=url, alt='foto', style={'height': '40%', 'width': '40%'}),
                html.Div([
                    html.Span(m.name, style={'font-weight': 'bold', 'size': 50, 'margin': 5}),
                    html.Span('Birthday: ' + birthday, style={'font-style': 'italic', 'size': 12, 'margin': 5}),
                    html.Span('Place of birth: ' + place_of_birth,
                              style={'font-style': 'italic', 'size': 12, 'margin': 5}),
                    html.Span('Biography: ' + biography, style={'font-weight': 'normal', 'size': 6, 'margin': 5}),
                    html.Span('Gender: ' + gender, style={'font-style': 'italic', 'size': 9, 'margin': 3}),
                    html.Span('Known for department: ' + known_for_department,
                              style={'font-style': 'italic', 'size': 9, 'margin': 3}),
                    html.Span('Popularity: ' + popularity, style={'font-style': 'italic', 'size': 9, 'margin': 3}),
                    html.Div([
                        html.Span('Movies:', style={'font-style': 'italic', 'size': 9, 'margin': 3}),
                        html.Ul(movies_list, style={'font-style': 'normal', 'size': 9, 'margin': 3})
                    ]),
                ],
                    style={"display": "flex", "flex-direction": "column"}
                )],
                style={"display": "flex", "flex-direction": "row", 'margin': 10, "background": "gainsboro"}
            ),
        ]
        # children.append(new_item)
        return new_item
