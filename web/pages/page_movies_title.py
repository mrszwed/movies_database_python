from datetime import date

import sqlalchemy
from dash import Dash, html, dcc, Input, Output, State, callback
from sqlalchemy.orm import Session

import configuration
from queries.query_movies import select_movies_by_title
from web.format_results import to_web_list
from web.pages.menu_bar import menu_bar

layout = html.Div([
    menu_bar(add_root=True),
    html.H2('Movies by title and date'),
    html.Div([
        html.Div([
            html.Label('Title', style={'margin-right': 10}),
            dcc.Input(id='q1_title', type='text', value=''),
        ], style={"display": "flex", "flex-direction": "column", "margin": 20}),
        html.Div([
            html.Label('Date from', style={'margin-right': 10}),
            dcc.DatePickerSingle(
                id='q1_date_from',
                min_date_allowed=date(1900, 1, 1),
                max_date_allowed=date(2030, 1, 1),
                initial_visible_month=date(1990, 1, 1),
            ),
        ], style={"display": "flex", "flex-direction": "column", "margin": 20}),
        html.Div([
            html.Label('Date to', style={'margin-right': 10}),
            dcc.DatePickerSingle(
                id='q1_date_to',
                min_date_allowed=date(1900, 1, 1),
                max_date_allowed=date(2030, 1, 1),
                initial_visible_month=date(2022, 1, 1),
            ),
        ], style={"display": "flex", "flex-direction": "column", "margin": 20}),
    ], style={"display": "flex", "flex-direction": "row"}),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    # html.Div(id='output-state'),
    html.Ul(id='list-container-mt', children=[], style={'list-style-type': 'none'}),
    html.Br(),

])


@callback(Output('list-container-mt', 'children'),
          Input('submit-button', 'n_clicks'),
          State('q1_title', 'value'),
          State('q1_date_from', 'date'),
          State('q1_date_to', 'date'),
          )
def update_output(n_clicks, title, date_from, date_to):
    if title == '':
        return [html.Li(children=[html.Span("No matching movies")])]
    if date_from == '':
        date_from = None
    if date_to == '':
        date_to = None

    engine = sqlalchemy.create_engine(configuration.conn_string)
    with Session(engine) as session:
        movies = select_movies_by_title(session=session, title=title, date_from=date_from, date_to=date_to)
        children = to_web_list(movies)
        return children
    return []
