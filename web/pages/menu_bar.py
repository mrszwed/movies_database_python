from dash import Dash, html, dcc, Input, Output, State, callback


def menu_bar(add_root=False):
    items = [
        dcc.Link('Movies by title', href='/movies_title', style={'margin': 10}),
        dcc.Link('Movies by actor', href='/movies_actor', style={'margin': 10}),
        dcc.Link('Movies by genres', href='/movies_genres', style={'margin': 10}),
        dcc.Link('Movies by extracted NERs', href='/movies_extracted_ner', style={'margin': 10}),
        dcc.Link('Movies by named entities', href='/movies_named_entities', style={'margin': 10}),
        dcc.Link('Movies from NLP', href='/movies_natural_language', style={'margin': 10}),
        dcc.Link('People by name', href='/people_name', style={'margin': 10}),
        dcc.Link('Actors from movies', href='/people_actor', style={'margin': 10}),
        dcc.Link('Crew from movies', href='/people_crew', style={'margin': 10}),
    ]
    if add_root:
        items.insert(0, dcc.Link('Root', href='/', style={'margin': 10}))
    return html.Div(items, style={"display": "flex", "flex-direction": "row", 'margin': 10})
