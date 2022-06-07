from datetime import date

import sqlalchemy
from dash import Dash, html, dcc, Input, Output, State, callback
from sqlalchemy.orm import Session
from feeding_db import ner_extraction
import configuration
from natural_language.spacy_nlp import SpacyNlp
from queries.query_movies import select_movies_by_title
from web.format_results import to_web_list, to_web_list_movie_details, to_web_list_person_details
from web.pages import page_movies_title, page_movies_people, page_movies_genres, page_movies_named_entities, \
    page_people_name, page_people_actor, page_people_crew, page_movies_extracted_ner, page_movies_natural_language
from web.pages.menu_bar import menu_bar

app = Dash(__name__)
app.config.suppress_callback_exceptions = True
nlp = SpacyNlp().get()

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

layout_index = menu_bar()


# Index callbacks
@callback(Output('page-content', 'children'),
          Input('url', 'pathname'))
def display_page(pathname):
    if pathname == "/movies_title":
        return page_movies_title.layout
    elif pathname == "/movies_actor":
        return page_movies_people.layout
    elif pathname == "/movies_genres":
        return page_movies_genres.layout
    elif pathname == "/movies_named_entities":
        return page_movies_named_entities.layout
    elif pathname == "/movies_extracted_ner":
        return page_movies_extracted_ner.layout
    elif pathname == "/movies_natural_language":
        return page_movies_natural_language.layout
    elif pathname == "/people_name":
        return page_people_name.layout
    elif pathname == "/people_actor":
        return page_people_actor.layout
    elif pathname == "/people_crew":
        return page_people_crew.layout
    elif pathname.startswith('/movie/'):
        id = int(pathname.replace("/movie/", ""))
        return to_web_list_movie_details(id)
    elif pathname.startswith('/person/'):
        id = int(pathname.replace("/person/", ""))
        return to_web_list_person_details(id)
    else:
        return layout_index


if __name__ == '__main__':
    app.run_server(debug=True)
