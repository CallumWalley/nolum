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
import hashlib

from dash.dependencies import Input, Output

from OSMPythonTools.nominatim import Nominatim

# Where to look for data.
dataPath = "data"
db_placeholder = [
        {"name": "06-0169-0179253-04_Transactions_2019-02-16_2019-12-31.csv", "hd5sum": "fake", "path":"data"}]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def get_bullshit():
    try:
        return [html.Q(children=re.search(r'\n<li>(.*)</li>', urllib.request.urlopen('http://cbsg.sf.net').read().decode('UTF-8')).group(1)), html.P(children=' - Noel Zeng')]
    except:
        return ":("


def ls(dataPath):
    outlist = []
    for file in os.listdir(dataPath):
        newpath = os.path.join(dataPath, file)
        if os.path.isdir(newpath):
            for f in ls(newpath):
                outlist.append(f)
        elif newpath[-4:].lower() == ".csv":
            hd5sum = hashlib.md5(open(newpath).read().encode('utf-8')).hexdigest()
            # if file in map(lambda x: x["name"], db_placeholder)
            # If in database, but hex different, add to csv_files_digested_changed.
            # If in database, don't add.
            splitpath=list(os.path.split(newpath))
            name=splitpath.pop()
            path="/".join(splitpath)
            outlist.append({"name":name, "path":path, "hd5sum":hd5sum})
    return outlist


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
                    options=[{'label': 'placeholder', 'value': 'placeholder'}],
                    placeholder="Select account"
                    # options=list(
                    #     map(lambda x: {'label': x, 'value': x}, os.listdir(dataPath))),
                )
            ]),
            html.Div(id="file-select-tables", children=[
                html.Div(className="file-select-table", children=[
                    html.Div(className="injest-file-header", children=[
                        html.P("Undigested input files"),
                        html.Button(
                            '⟳', id='injest-file-selector-refresh-button', className="refresh-button")
                    ]),
                    html.Div(className='radio-scroll', id='injest-file-selector-wrap',
                             children=[dcc.Checklist(
                                 id='injest-file-selector'
                             )]),
                ]),
                html.Div(className="file-select-table", children=[
                    html.Div(className="injest-file-header", children=[
                        html.P("Digested input files"),
                        html.Button(
                            '⟳', id='injest-file-display-refresh-button', className="refresh-button")
                    ]),
                    html.Div(className='radio-scroll', id='injest-file-display-wrap',
                             children=[dcc.Checklist(
                                 id='injest-file-display'
                             )]),
                ]),
            ]),
            html.Div(id='injest-tag-table-wrap'),
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
    dash.dependencies.Output('injest-file-selector', 'options'),
    dash.dependencies.Input('injest-file-selector-refresh-button', 'value'))
def updateFileSelector(unused):
    allFiles=list(map(lambda x: x["name"], ls(dataPath)))
    dbFiles=list(map(lambda x: x["name"], db_placeholder))

    newFiles = filter(lambda x: x not in dbFiles, allFiles)

    return list(map(lambda x: {'label': x, 'value': x}, newFiles))

@ app.callback(
    dash.dependencies.Output('injest-file-display', 'options'),
    #dash.dependencies.Output('injest-file-display', 'options'),
    dash.dependencies.Input('injest-file-selector-refresh-button', 'value'))
def updateFileDisplay(unused):

    # fileSelector=dcc.Checklist(
    #     id='file-selector',
    #     className='account-selector',
    #     options=list(map(lambda x: {'label': x, 'value': x}, csv_files_undigested))
    # )

    return list(map(lambda x: {'label': x, 'value': x}, map(lambda x: x["name"], db_placeholder)))


# Called when input file selected, updates tag table
@ app.callback(
    dash.dependencies.Output('injest-tag-table-wrap', 'children'),
    dash.dependencies.Input('injest-file-selector', 'value'))
def updateTagTable(input_files):
    

    full_list = []

    if input_files:
        for input_file in input_files:
            try:
                with open(input_file) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for line in csv_reader:
                        full_list.append(list(line) + [input_file])
            except:
                pass

    dataTable = dash_table.DataTable(
        id='table',
        columns=[
            #{"name": "ID", "id": "id"},
            {"name": "Date",  "id": "date", "type": "datetime"},
            {"name": "From", "id": "from_account", 'presentation': 'dropdown'},
            {"name": "To", "id": "to_account", 'presentation': 'dropdown'},
            {"name": "Amount", "id": "amount", "type": "numeric"},
            {"name": "Type", "id": "pay_type", },
            {"name": "Tags", "id": "tags"},
            {"name": "Details", "id": "details"},
            #{"name": "Source", "id": "source"},
            #{"name": "Raw String", "id": "raw_string"},
            {"name": "Confidence", "id": "confidence"}
        ],
        # INSERT MACHINE LEARNING HERE
        data=list(map(lambda x: {
            "include": True,
            "date": x[6],
            "amount": x[5],
            "pay_type": x[0],
            "tags": "",
            "details": str([x[1] + x[2] + x[3] + x[4]]),
            "confidence": 0,
            # "source":input_file,
            # "raw_string": str(x)
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

    return dataTable

# Tabs


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
