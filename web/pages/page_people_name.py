from datetime import date

import sqlalchemy
from dash import Dash, html, dcc, Input, Output, State, callback
from sqlalchemy.orm import Session

import configuration
from queries.query_movies import select_movies_by_title
from queries.query_people import select_people
from web.format_results import to_web_list, to_web_list_people
from web.pages.menu_bar import menu_bar

layout = html.Div([
    menu_bar(add_root=True),
    html.H2('People by name, place of birth and birthday'),
    html.Div([
        html.Div([
            html.Label('Name', style={'margin-right': 10}),
            dcc.Input(id='q1_name', type='text', value=''),
        ], style={"display": "flex", "flex-direction": "column", "margin": 20}),
        html.Div([
            html.Label('Place of birth', style={'margin-right': 10}),
            dcc.Input(id='q1_place_of_birth', type='text', value=''),
        ], style={"display": "flex", "flex-direction": "column", "margin": 20}),
        html.Div([
            html.Label('Birthday from', style={'margin-right': 10}),
            dcc.DatePickerSingle(
                id='q1_birthday_from',
                min_date_allowed=date(1900, 1, 1),
                max_date_allowed=date(2023, 1, 1),
                initial_visible_month=date(1960, 1, 1),
            ),
        ], style={"display": "flex", "flex-direction": "column", "margin": 20}),
        html.Div([
            html.Label('Birthday to', style={'margin-right': 10}),
            dcc.DatePickerSingle(
                id='q1_birthday_to',
                min_date_allowed=date(1900, 1, 1),
                max_date_allowed=date(2023, 1, 1),
                initial_visible_month=date(2000, 1, 1),
            ),
        ], style={"display": "flex", "flex-direction": "column", "margin": 20}),
    ], style={"display": "flex", "flex-direction": "row"}),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Ul(id='list-container-pn', children=[], style={'list-style-type': 'none'}),
    html.Br(),

])


@callback(Output('list-container-pn', 'children'),
          Input('submit-button', 'n_clicks'),
          State('q1_name', 'value'),
          State('q1_place_of_birth', 'value'),
          State('q1_birthday_from', 'date'),
          State('q1_birthday_to', 'date'),
          )
def update_output(n_clicks, name, place_of_birth, birthday_from, birthday_to):
    if name == '':
        return [html.Li(children=[html.Span("No matching people")])]
    if place_of_birth == '':
        place_of_birth = None
    if birthday_from == '':
        birthday_from = None
    if birthday_to == '':
        birthday_to = None

    engine = sqlalchemy.create_engine(configuration.conn_string)
    with Session(engine) as session:
        people = select_people(session=session, name=name, place_of_birth=place_of_birth, date_from=birthday_from,
                               date_to=birthday_to)
        children = to_web_list_people(people)
        return children
    return []
