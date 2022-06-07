from datetime import date

import sqlalchemy
from dash import Dash, html, dcc, Input, Output, State, callback
from sqlalchemy.orm import Session

import configuration
from queries.query_movies import select_movies_by_title
from queries.query_people import select_people, select_actors_from_movie
from web.format_results import to_web_list, to_web_list_people, to_web_list_actors
from web.pages.menu_bar import menu_bar

layout = html.Div([
    menu_bar(add_root=True),
    html.H2('Actors from movie'),
    html.Div([
        html.Div([
            html.Label('Title', style={'margin-right': 10}),
            dcc.Input(id='q1_title', type='text', value=''),
        ], style={"display": "flex", "flex-direction": "column", "margin": 20}),
    ], style={"display": "flex", "flex-direction": "row"}),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Ul(id='list-container-am', children=[], style={'list-style-type': 'none'}),
    html.Br(),

])


@callback(Output('list-container-am', 'children'),
          Input('submit-button', 'n_clicks'),
          State('q1_title', 'value'),
          )
def update_output(n_clicks, title):
    if title == '':
        return [html.Li(children=[html.Span("No matching people")])]

    engine = sqlalchemy.create_engine(configuration.conn_string)
    with Session(engine) as session:
        people = select_actors_from_movie(session=session, title=title)
        children = to_web_list_actors(people)
        return children
    return []
