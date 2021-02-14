# -*- coding: utf-8 -*-

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import os
import re
import csv
import urllib.request

from dash.dependencies import Input, Output

# Where to look for data.
dataPath = "data"

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def get_bullshit():
    try:
        return [html.Q(children=re.search(r'\n<li>(.*)</li>', urllib.request.urlopen('http://cbsg.sf.net').read().decode('UTF-8')).group(1)), html.P(children=' - Noel Zeng')]
    except:
        return ":("


app.layout = html.Div(children=[
    html.H1(children='NoLum Cloud-Native Deep-Learning Hyper-Ledger'),
    html.Div(id='daily-wisdom', children=get_bullshit()),
    html.Div(id='operations', children=[
        html.H2(children='Operations'),
        html.Div(id='op-ingest', children=[
            html.H3(children="Ingest new data"),
            html.Div(children=[
                html.Label(children="Target Account"),
                dcc.Dropdown(
                    id='ingest-select-account',
                    className='account-selector',
                    options=[{'label': 'placeholder', 'value': 'placeholder'}]
                    # options=list(
                    #     map(lambda x: {'label': x, 'value': x}, os.listdir(dataPath))),
                )
            ]),
            html.Div(className='radio-scroll', children=[
                dcc.Checklist(
                    id='ingest-list',
                    options=list(
                        map(lambda x: {'label': x, 'value': x}, os.listdir(dataPath))),
                    value=[]  # List of imported documents.
                )
            ]),
            html.Button('Load', id='load-button', n_clicks=0),
            html.Div(id='ingest-tag-table'),
            html.Button('Ingest', id='ingest-button', n_clicks=0),
            html.Div(id='ingested-data')

        ])
    ]),
    html.Div(id='metrics', children=[
        html.H2(children='Metrics'),
        dcc.Tabs(id='metrics-tab', value='tab-1', children=[
            dcc.Tab(label='placeholder', value='tab-1'),
            dcc.Tab(label='placeholder', value='tab-2'),
        ]),
        html.Div(id='metrics-tab-content')
    ])
])


@ app.callback(
    dash.dependencies.Output('ingest-tag-table', 'children'),
    dash.dependencies.Input('load-button', 'n_clicks'),
    dash.dependencies.State('ingest-list', 'value'))

def update_output(clicks, input_files):
    full_list = []
    for input_file in input_files:
        with open(os.path.join(dataPath, input_file)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for line in csv_reader:
                full_list.append(list(line) + [input_file])
    return dash_table.DataTable(
        id='table',
        columns=[
            #{"name": "ID", "id": "id"}, 
            {"name": "Date",  "id": "date"},
            {"name": "From", "id": "from_account",'presentation': 'dropdown'},
            {"name": "To", "id": "to_account",'presentation': 'dropdown'},
            {"name": "Amount", "id": "amount"},
            {"name": "Type", "id": "pay_type",},
            {"name": "Tags", "id": "tags"},
            {"name": "Details", "id": "details"},
            #{"name": "Source", "id": "source"},
            #{"name": "Raw String", "id": "raw_string"},
            {"name": "Confidence", "id": "confidence"}
        ],
        # INSERT MACHINE LEARNING HERE
        data=list(map(lambda x: {
            "include": True,
            "date":x[6],
            "amount":x[5],
            "pay_type":x[0], 
            "tags":"", 
            "details":str([x[1] + x[2] + x[3] + x[4]]),
            "confidence":0,
            #"source":input_file,
            #"raw_string": str(x)
            }, full_list)),
        
        # utilities
        #   power
        #   rent
        #   water
        # essentials
        #   food
        #   coffee
        # fribble
        #   games
        #   activities
        # income
        #   salary
        #   invoices
        # misc
        #   misc 
        # 
        #

        dropdown={
            'from_account': {
                'options': [
                    {'label': "placeholder", 'value': 'placeholder'}
                ]
            },
            'to_account': {
                'options': [
                    {'label': "placeholder", 'value': 'placeholder'}
                ]
            }
        },
        row_selectable='multi',
        selected_rows=[i for i in range(len(full_list))],
        editable=True
    )


@app.callback(Output('metrics-tab-content', 'children'),
              Input('metrics-tab', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('placeholder')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('placeholder')
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
