from datetime import date

import sqlalchemy
from dash import Dash, html, dcc, Input, Output, State, callback
from sqlalchemy.orm import Session

import configuration
from queries.query_movies import select_movies_by_title, select_movies_by_actor_name, select_movies_by_genres_and
from web.format_results import to_web_list, to_web_list_with_actors, to_web_list_with_genres
from web.pages.menu_bar import menu_bar

layout = html.Div([
    menu_bar(add_root=True),
    html.H2('Movies by genre'),
    html.Div([
        html.Div([
            html.Label('Genres', style={'margin-right': 10}),
            dcc.Input(id='q1_genre', type='text', value='', size='100'),
        ], style={"display": "flex", "flex-direction": "column", "margin": 20}),
        html.Div([
            html.Label('Limit', style={'margin-right': 10}),
            dcc.Input(id='q1_limit', type='number', value='100', ),
        ], style={"display": "flex", "flex-direction": "column", "margin": 20}),
    ], style={"display": "flex", "flex-direction": "row"}),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    # html.Div(id='output-state'),
    html.Ul(id='list-container-mg', children=[], style={'list-style-type': 'none'}),
    html.Br(),

])


@callback(Output('list-container-mg', 'children'),
          Input('submit-button', 'n_clicks'),
          State('q1_genre', 'value'),
          State('q1_limit', 'value'),
          )
def update_output(n_clicks, genre, limit):
    if genre == '':
        return [html.Li(children=[html.Span("No matching movies")])]
    if limit == '':
        limit = 100

    engine = sqlalchemy.create_engine(configuration.conn_string)
    with Session(engine) as session:
        genre = genre.replace(',', ' ')
        genre = genre.split()
        movies = select_movies_by_genres_and(session=session, genres=genre, limit=limit)
        children = to_web_list_with_genres(movies)
        return children
    return [html.Li(children=[html.Span("No matching movies")])]
