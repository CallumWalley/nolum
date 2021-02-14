# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

stylesheets = ['style.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(children=[
    html.H1(children='nolum'),
    html.h2(children='')
])

if __name__ == '__main__':
    app.run_server(debug=True)