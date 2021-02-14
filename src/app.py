# -*- coding: utf-8 -*-

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import os
import re
import urllib.request

from dash.dependencies import Input, Output

# Where to look for data.
dataPath = "data"

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def get_bullshit():
    try:
        return [html.Q(children=re.search(r'\n<li>(.*)</li>', urllib.request.urlopen('http://cbsg.sf.net').read().decode('UTF-8')).group(1)),html.P(children=' - Noel Zeng')] 
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
                    options = [{'label':'placeholder', 'value':'placeholder'}]
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
            html.Button('Ingest', id='ingest-button', n_clicks=0),
            html.Div(id='ingest-tag-table'),
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
    dash.dependencies.Input('ingest-button', 'n_clicks'),
    dash.dependencies.State('ingest-list', 'value'))
def update_output(clicks, input_files):
    df_list= []
    for input_file in input_files:
        df_list.append(pd.read_csv(os.path.join(dataPath,input_file)))
    concatted_df=pd.concat(df_list, axis=0, ignore_index=True)
    return dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in concatted_df.columns],
        data=concatted_df
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
