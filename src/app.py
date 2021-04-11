# -*- coding: utf-8 -*-

import dash
import dash_table
import dash_tabulator
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import os
import re
import csv
import json
import urllib.request
import hashlib
import model as mdl
from datetime import date


from dash.dependencies import Input, Output
from dash_extensions.javascript import Namespace

from OSMPythonTools.nominatim import Nominatim

# Where to look for data.
dataPath = "data"
ns_tab = Namespace("dashlyNamespace", "tabulator")

db_placeholder = [
    {"name": "06-0169-0179253-04_Transactions_2019-02-16_2019-12-31.csv", "md5sum": "fake", "path": "data"}]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Set up connection with database
DbSession = mdl.create_session_maker()

transaction_types = ["credit", "transfer",
                     "illegal drugs", "Bank Fee", "Visa Purchase"]
# class DataTable(dash_table.DataTable):
foundInputFiles = {}

def ls(dataPath):
    outlist = []
    for file in os.listdir(dataPath):
        newpath = os.path.join(dataPath, file)
        if os.path.isdir(newpath):
            for f in ls(newpath):
                outlist.append(f)
        elif newpath[-4:].lower() == ".csv":
            hd5sum = hashlib.md5(
                open(newpath).read().encode('utf-8')).hexdigest()
            # if file in map(lambda x: x["name"], db_placeholder)
            # If in database, but hex different, add to csv_files_digested_changed.
            # If in database, don't add.
            outlist.append({"name": newpath, "hd5sum": hd5sum})
    return outlist


def find_input_files_by_name():
    # Builds and returns metadata for files in the data path.
    files = ls(dataPath)
    files_by_name = {}
    for file in files:
        files_by_name[file["name"]] = file
    return files_by_name


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
                    html.Div(className="injest-file-header pseudo-dash", children=[
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
                    html.Div(className="injest-file-header pseudo-dash", children=[
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
    dash.dependencies.Output('ingested-data', 'children'),
    dash.dependencies.Input('ingest-button', 'n_clicks'),
    dash.dependencies.State('injest-file-selector', "value"),
    dash.dependencies.State('injest-tag-table-wrap', "children"))
def injestDoc(nothing, inputSource, everythin):
    input_files_by_name = find_input_files_by_name()
    # print("My input source is " + str(inputSource))
    # print(list(filter(lambda x: x["name"]==inputSource, foundInputFiles)))
    if inputSource is None:
        return
    session = DbSession()
    for source in inputSource:
        matched_file = input_files_by_name[source]
        filename = os.path.basename(source)
        ingestion_date = date.today()
        hd5sum = matched_file["hd5sum"]
        if len(session.query(mdl.InputSource).filter(mdl.InputSource.path == source).all()) > 0:
            # Skip ingest if already imported
            print(f"Skipping import for {filename} as already in database.")
            continue
        session.add(mdl.InputSource(path=source, filename=filename,
                                    hd5sum=hd5sum, ingest_date=ingestion_date))
    # Save all to the session
    print(f"Committing {len(session.new)} object(s) into database.")
    session.commit()
    session.close()


@ app.callback(
    dash.dependencies.Output('injest-file-selector', 'options'),
    dash.dependencies.Input('injest-file-selector-refresh-button', 'value'))
def updateFileSelector(unused):
    foundInputFiles = ls(dataPath)
    newFiles = filter(lambda x: x['name'] not in map(
        lambda y: y["name"], db_placeholder), foundInputFiles)

    return list(map(lambda x: {'label': x["name"], 'value': x["name"]}, newFiles))


@ app.callback(
    dash.dependencies.Output('injest-file-display', 'options'),
    #dash.dependencies.Output('injest-file-display', 'options'),
    dash.dependencies.Input('injest-file-display-refresh-button', 'value'))
def updateFileDisplay(unused):

    # fileSelector=dcc.Checklist(
    #     id='file-selector',
    #     className='account-selector',
    #     options=list(map(lambda x: {'label': x, 'value': x}, csv_files_undigested))
    # )

    return list(map(lambda x: {'label': x, 'value': x}, map(lambda x: x["name"], db_placeholder)))


# For suggesting entities
html.Datalist(
    id='entity-datalist',
    children=[html.Option(value=word) for word in ["entity1", "entity2", "entity3", "entity4"]])
# Called when input file selected, updates tag table


@ app.callback(
    dash.dependencies.Output('injest-tag-table-wrap', 'children'),
    dash.dependencies.Input('injest-file-selector', 'value'))
def updateTagTable(input_files):
    fullList = []
    # ns = Namespace("myNamespace", "tabulator")

    if input_files:
        for input_file in input_files:
            # try:
            with open(input_file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for line in csv_reader:
                    fullList.append(list(line) + [input_file])
            # except:
            #     print("fuc")
    # columns = [
    #             { "title": "Name", "field": "name", "width": 150, "headerFilter":True, "editor":"input"},
    #             { "title": "Age", "field": "age", "hozAlign": "left", "formatter": "progress" },
    #             { "title": "Favourite Color", "field": "col", "headerFilter":True },
    #             { "title": "Date Of Birth", "field": "dob", "hozAlign": "center" },
    #             { "title": "Rating", "field": "rating", "hozAlign": "center", "formatter": "star" },
    #             { "title": "Passed?", "field": "passed", "hozAlign": "center", "formatter": "tickCross" }
    #           ]
    columns = [
        #{"name": "ID", "id": "id"},
        {"title": "Import", "field": "include", "sorter": "boolean",
            "editor": True, "formatter": "tickCross", "tooltip": "Tooltip!"},
        {"title": "Date", "field": "date", "sorter": "date", "sorterParams": {
            "format": "YYYY-MM-DD"}, "tooltip": "Tooltip!"},
        {"title": "From", "field": "from", 
            "sorter": "alphanum", "editor": "autocomplete", "tooltip": "Tooltip!", "editorParams":{
                "freetext":True, "showListOnEmpty":True, "values":["person1", "person2", "person3"], "searchFunc":ns_tab("fromFreetext"),
            }},
        {"title": "To", "field": "to", "editor": True, "tooltip": "Tooltip!"},
        {"title": "Amount", "field": "amount", "sorter": "number",
            "formatter": "money", "editor": True, "tooltip": "Tooltip!"},
        {"title": "Type", "field": "pay_type", "tooltip": "Tooltip!",
            "editor": "select", "editorParams": {"values": transaction_types}},
        {"title": "Tags", "field": "tags", "tooltip": "Tooltip!"},
        {"title": "Details", "field": "details", "tooltip": "Tooltip!"},
        {"name": "Source", "id": "source"},
        {"name": "Raw String", "id": "raw_string"},
        {"title": "Confidence", "field": "confidence"}
    ]
    data = list(map(lambda x: {
        "include": True,
        "date": x[6],
        "amount": x[5],
        "pay_type": x[0],
        "tags": "",
        "details": str([x[1] + x[2] + x[3] + x[4]]),
        "confidence": 0,
        # "source":input_file,
        # "raw_string": str(x)
    }, fullList))
    options = {
            "formatter": ns_tab("printIcon")
        }
    # Setup some data
    # data = [
    #                 {"id":1, "name":"Oli Bob", "age":"12", "col":"red", "dob":""},
    #                 {"id":2, "name":"Mary May", "age":"1", "col":"blue", "dob":"14/05/1982"},
    #                 {"id":3, "name":"Christine Lobowski", "age":"42", "col":"green", "dob":"22/05/1982"},
    #                 {"id":4, "name":"Brendon Philips", "age":"125", "col":"orange", "dob":"01/08/1980"},
    #                 {"id":5, "name":"Margret Marmajuke", "age":"16", "col":"yellow", "dob":"31/01/1999"},
    #                 {"id":6, "name":"Fred Savage", "age":"16", "col":"yellow", "rating":"1", "dob":"31/01/1999"},
    #                 {"id":6, "name":"Brie Larson", "age":"30", "col":"blue", "rating":"1", "dob":"31/01/1999"},
    #             ]

    dataTable = dash_tabulator.DashTabulator(
        id='injest-tag-table',
        columns=columns,
        data=data,
        options=options
    )
    # def genRow(index, input):
    #     def plainTextFixed(value):
    #         return html.Td(value)
    #     def plainTextEntity(value):
    #         return html.Td(
    #             dcc.Input(
    #                 type='text',
    #                 list='entity-datalist',
    #                 value=value
    #             )
    #         )
    #     def strikeoutButton():
    #         return html.Td(
    #                 html.Button('x',id=f"strikeout-button-{index}", className="strikeout-button")
    #             )

    #     return html.Tr(children=[
    #         strikeoutButton(),
    #         plainTextFixed(input[0]),
    #         plainTextEntity(input[1]),
    #         plainTextEntity(input[2]),
    #         plainTextFixed(input[3]),
    #         plainTextFixed(input[4]),
    #         plainTextFixed(input[5]),
    #         plainTextFixed(input[6]),
    #         plainTextFixed(input[7]),
    #         plainTextFixed(input[8]),
    #         plainTextFixed(input[9])
    #     ])

    # columns = ["Date", "From", "To", "Amount", "Type", "Tags", "Details", "Source", "RawString", "Confidence"]
    # #dash_table.DataTable(
    # dataTable=html.Table(id="injest-tag-table",style={"width":"100%"}, children=[
    #     html.Thead(style={"width":"100%"}, className="pseudo-dash", children=list(map(lambda x: html.Th(x), columns))),
    #     html.Tbody(children=[*list(genRow(i,l) for i,l in enumerate(fullList))])
    #     # html.Tbody(*list(map(genRow,fullList)))

    # ])

    #     # INSERT MACHINE LEARNING HERE
    #

    #     # utilities
    #     #   power
    #     #   rent
    #     #   water
    #     # essentials
    #     #   food
    #     #   coffee
    #     # fribble
    #     #   games
    #     #   activities
    #     # income
    #     #   salary
    #     #   invoices
    #     # misc
    #     #   misc
    #     #
    #     #

    #     # dropdown={
    #     #     'from_account': {
    #     #         'options': [
    #     #             {'label': "placeholder", 'value': 'placeholder'}
    #     #         ]
    #     #     },
    #     #     'to_account': {
    #     #         'options': [
    #     #             {'label': "placeholder", 'value': 'placeholder'}
    #     #         ]
    #     #     }
    #     # },
    #     row_selectable='multi',
    #     selected_rows=[i for i in range(len(full_list))],
    #     editable=True
    # )

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
