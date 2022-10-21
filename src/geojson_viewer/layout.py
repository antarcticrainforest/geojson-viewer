"""Definitions of the dash layout."""

from pathlib import Path
from dash import Dash, dcc, dash_table, html


display_tab = [
    html.Div(
        children=[
            dcc.Upload(
                id="upload",
                children=html.Div(
                    [
                        "First Drag and Drop ",
                        html.A("/ click to select a File"),
                    ]
                ),
                style={
                    "width": "100%",
                    "height": "60px",
                    "lineHeight": "60px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "margin": "10px",
                },
            ),
        ]
    ),
    html.Div(
        children=[
            html.Label("or set a URL", className="input"),
            dcc.Input(
                id="geojson-file",
                type="text",
                className="input",
            ),
            html.Button(
                id="load-button",
                n_clicks=0,
                children="Load url",
                className="input",
            ),
            html.Label("then select two data keys:", className="input"),
            html.Div(
                style={"min-width": "50%"},
                children=[
                    dcc.Dropdown(
                        id="column1",
                        multi=True,
                        className="input",
                    ),
                ],
            ),
        ],
        style={"padding": 10, "display": "flex"},
    ),
    html.Div(
        [
            dcc.Loading(
                id="loading1",
                type="circle",
                className="input",
                children=html.P(id="load-status", style={"color": "red"}),
            ),
            html.Button(
                id="view-button",
                n_clicks=0,
                children="View",
                className="input",
            ),
            dcc.Loading(
                id="loading2",
                type="default",
                className="input",
                children=html.P(id="view-status"),
            ),
            html.Br(),
            html.Div(id="graph-box", children=[dcc.Graph(id="graph")]),
        ]
    ),
]

edit_tab = [
    html.Div(
        id="edit-buttons",
        style={"padding": 10, "display": "flex"},
        children=[
            dcc.Download(id="download-geojson"),
            html.Button(
                id="save-button",
                children="Save data",
                n_clicks=0,
                disabled=True,
                className="input",
            ),
            html.Button(
                id="reset-button",
                children="Reset data",
                disabled=True,
                n_clicks=0,
                className="input",
            ),
        ],
    ),
    dcc.Loading(id="loading3", type="circle", className="input", children=[]),
    html.Div(
        id="table-box",
        children=[
            html.P(
                "Load geojson file in the display tab first",
                style={"color": "black"},
            ),
            html.Br(),
            dash_table.DataTable(id="table"),
        ],
    ),
]
