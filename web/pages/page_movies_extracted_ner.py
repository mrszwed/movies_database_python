from datetime import date

import sqlalchemy
from dash import Dash, html, dcc, Input, Output, State, callback
from sqlalchemy.orm import Session

import configuration
from feeding_db.ner_extraction import extract_NERs
from queries.query_movies import select_movies_by_title, select_movies_by_actor_name, select_movies_by_genres_and, \
    select_movies_by_named_entities_and, select_movies_by_named_entities, select_movies_by_named_entities_or
from web.format_results import to_web_list, to_web_list_with_actors, to_web_list_with_genres, \
    to_web_list_with_named_entities
from web.pages.menu_bar import menu_bar

layout = html.Div([
    menu_bar(add_root=True),
    html.H2('Movies by extracted named entities'),
    html.Div([
        html.Div([
            html.Label('Search movies', style={'margin-right': 10}),
            dcc.Input(id='q1_named_entities', type='text', value='', size='100'),
        ], style={"display": "flex", "flex-direction": "column", "margin": 20}),
    ], style={"display": "flex", "flex-direction": "row"}),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Ul(id='list-container-ene', children=[], style={'list-style-type': 'none'}),
    html.Br(),

])


@callback(Output('list-container-ene', 'children'),
          Input('submit-button', 'n_clicks'),
          State('q1_named_entities', 'value'),
          )
def update_output(n_clicks, named_entities):
    if named_entities == '':
        return [html.Li(children=[html.Span("No matching movies")])]

    engine = sqlalchemy.create_engine(configuration.conn_string)
    with Session(engine) as session:
        named_entities = extract_NERs(named_entities, False)
        entities_text = [e[0] for e in named_entities]
        movies = select_movies_by_named_entities_or(session=session, entities=entities_text)
        children = to_web_list_with_named_entities(movies, named_entities)
        return children
    return [html.Li(children=[html.Span("No matching movies")])]
