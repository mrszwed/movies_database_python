from dash import Dash, html, dcc, Input, Output, State, callback

layout = html.Div([
    dcc.Link('Query Movies"', href='/movies'),
    html.Br(),
    dcc.Link('Query People"', href='/people'),
])

# Index callbacks
# @callback(Output('page-content', 'children'),
#           Input('url', 'pathname'))
# def display_page(pathname):
#     if pathname == "/movies":
#         return layout_movies
#     elif pathname == "/people":
#         return layout_people
#     else:
#         return layout_index
