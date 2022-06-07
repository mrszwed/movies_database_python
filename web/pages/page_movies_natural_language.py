from datetime import date

import sqlalchemy
from dash import Dash, html, dcc, Input, Output, State, callback
from sqlalchemy.orm import Session

import configuration
from feeding_db.ner_extraction import extract_NERs
from natural_language.matcher import MovieActorDate, MovieActor, MovieDirectorDate, MovieDirector
from natural_language.spacy_nlp import SpacyNlp
from queries.query_movies import select_movies_by_title, select_movies_by_actor_name, select_movies_by_genres_and, \
    select_movies_by_named_entities_and, select_movies_by_named_entities, select_movies_by_named_entities_or, \
    select_movies_by_actors_or, select_movies_directed_by, select_movies_by_two_actors
from web.format_results import to_web_list, to_web_list_with_actors, to_web_list_with_genres, \
    to_web_list_with_named_entities
from web.pages.menu_bar import menu_bar

nlp = SpacyNlp().get()

layout = html.Div([
    menu_bar(add_root=True),
    html.H2('Movies by natural language'),
    html.Div([
        html.Div([
            html.Label('Search movies', style={'margin-right': 10}),
            dcc.Input(id='q1_text', type='text', value='', size='100'),
        ], style={"display": "flex", "flex-direction": "column", "margin": 20}),
    ], style={"display": "flex", "flex-direction": "row"}),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Ul(id='list-container-nl', children=[], style={'list-style-type': 'none'}),
    html.Br(),

])


def _match(text):
    doc = nlp(text)
    matchers = [MovieActorDate(), MovieActor(), MovieDirectorDate(), MovieDirector()]
    for m in matchers:
        if m.match(doc):
            return m.get_results()
    return None


@callback(Output('list-container-nl', 'children'),
          Input('submit-button', 'n_clicks'),
          State('q1_text', 'value'),
          )
def update_output(n_clicks, text):
    if text == '':
        return [html.Li(children=[html.Span("No matching movies")])]

    engine = sqlalchemy.create_engine(configuration.conn_string)
    with Session(engine) as session:
        # named_entities=extract_NERs(named_entities, False)
        # entities_text = [e[0] for e in named_entities]

        result = _match(text)
        if result is None:
            return [html.Li(children=[html.Span("No matching movies")])]
        if result['match'] in ['MovieActorDate', 'MovieActor']:
            if result['personop'] == 'or':
                movies = select_movies_by_actors_or(session, result['persons'], result.get('date_first'),
                                                    result.get('date_second'))
            else:
                movies = select_movies_by_two_actors(session, result['persons'], result.get('date_first'),
                                                     result.get('date_second'))
        if result['match'] in ['MovieDirectorDate', 'MovieDirector']:
            movies = select_movies_directed_by(session, result['persons'], result.get('date_first'),
                                               result.get('date_second'))

        children = to_web_list(movies)
        matched_info = [html.Span(k + ': ' + str(result[k]),
                                  style={'background': '#73AD21', 'border-radius': '5px', 'padding': 7, 'margin': 5})
                        for k in result]
        children.insert(0, html.Li(children=matched_info))
        return children
    return [html.Li(children=[html.Span("No matching movies")])]
