"""Module containing all dash server callback methods."""

from __future__ import annotations
from datetime import datetime
from pathlib import Path
import json
from tempfile import NamedTemporaryFile
from typing import Any, cast

from dash import (
    ctx,
    Dash,
    dcc,
    dash_table,
    exceptions,
    html,
    Input,
    Output,
    State,
)
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import geopandas as gp
from .utils import GeoJsonFile, load_geojson, logger

app = Dash("geojson-viewer", assets_folder=Path(__file__).parent / "assets")


def _clear_fig(
    fig: go.Figure | None = None,
    text: str = "Choose 2 columns and click the view button to compare.",
) -> go.Figure:
    fig = go.Figure(fig or {})
    fig.update_layout(
        plot_bgcolor="white",
        xaxis=go.layout.XAxis(showticklabels=False),
        yaxis=go.layout.YAxis(showticklabels=False),
    )
    fig.add_annotation(
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        text=text,
        showarrow=False,
        align="center",
        font=dict(size=16),
    )
    return fig


geo_json_obj = GeoJsonFile()


@app.callback(
    Output("column1", "options"),
    Output("loading1", "children"),
    Output("table-box", "children"),
    Output("reset-button", "disabled"),
    Output("save-button", "disabled"),
    Output("geojson-file", "value"),
    Output("graph-box", "children"),
    State("geojson-file", "value"),
    Input("upload", "contents"),
    Input("reset-button", "n_clicks"),
    Input("load-button", "n_clicks"),
)
def create_columns(
    geojson_file: str | None, upload_content: str | None, *args: int
) -> tuple[list[str], html.P, list[Any], bool, bool, str, list[Any]]:
    """Create the dropdown menu for selecting the columns in the goejson file.

    Parameters
    ----------
    geojson_file: str
        The path (file path or url) to the geojson file that is going to be
        openend
    upload_content: str
        Any content that needs uploading and read

    Returns
    -------
    list:
        The data keys that should be displayed
    str:
        A message representing the status of opening the geojson file
    tuple:
        The elements of the view box that is displayed for editing the data
    """
    status_msg = ""
    disable_button = False
    if geojson_file is None and upload_content is None:
        return (
            [],
            html.P("", id="load-status"),
            geo_json_obj.to_viewbox(),
            True,
            True,
            "",
            [dcc.Graph(id="graph", figure=_clear_fig())],
        )
    if ctx.triggered_id == "load-button" or upload_content is not None:
        if ctx.triggered_id == "load-button":
            # Make sure only uploaded content or the url content is loaded
            upload_content = None
        else:
            geojson_file = None
        geo_json_obj.data_frame = None
        try:
            geo_json_obj.data_frame = load_geojson(
                geojson_file, upload_content
            )
        except Exception as error:
            logger.error(error)
            status_msg = "Error: Could not load data content"
    if geo_json_obj.data_frame is None:
        columns = []
        disable_button = True
    else:
        columns = [
            c for c in geo_json_obj.data_frame.columns if c != "geometry"
        ]

    return (
        columns,
        html.P(status_msg, id="load-status", style={"color": "red"}),
        geo_json_obj.to_viewbox(),
        disable_button,
        disable_button,
        geojson_file or "",
        [dcc.Graph(id="graph", figure=_clear_fig())],
    )


@app.callback(
    Output("graph", "figure"),
    Output("loading2", "children"),
    State("column1", "value"),
    State("table", "data"),
    Input("view-button", "n_clicks"),
)
def display_choropleth(
    columns: list[str | None] | None,
    table_data: list[dict[str, Any]],
    *args: int,
) -> tuple[go.Figure, str]:
    """Create the plot of the geojson data.

    The data that is displayed is taken from the table box rather than
    from the geojson data to be able to directly display any user modifications

    Parameters
    ----------
    columns: list | None
        List holding the entries that should be displayed
    table_data: list[dict]
        The data (taken from the table view box) of the table
        that should be displayed. This entry is needed to display any user
        modifications
    table_columns: list[str]
        The columns for the ``table_data```

    Returns
    ------
    go.Figure():
        The displayed figure
    str: The output state of the loading sign, this is used as a visual
        feedback for the user to wait while the figure is loading.
    """

    if columns is None or len(columns) != 2 or geo_json_obj.data_frame is None:
        return _clear_fig(), ""
    if len(columns) > 2:
        return _clear_fig(text="You should select only 2 data keys.")
    if columns[0] is None or columns[1] is None or columns[0] == columns[1]:
        return _clear_fig(), ""
    if columns[0] == columns[1]:
        return _clear_fig(text="Columns must be different"), ""

    location, color = cast(list[str], columns)
    data_frame = pd.DataFrame(table_data).astype(geo_json_obj.dtypes)
    try:
        geojson = json.loads(
            geo_json_obj.data_frame[[color, location, "geometry"]].to_json()
        )
    except KeyError:
        return _clear_fig(), ""
    fig = px.choropleth(
        data_frame,
        geojson=geojson,
        color=color,
        locations=location,
        color_continuous_scale="Viridis",
        featureidkey=f"properties.{location}",
    )
    fig.update_geos(projection_type="orthographic", fitbounds="locations")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig, ""


@app.callback(
    Output("download-geojson", "data"),
    State("table", "data"),
    State("table", "columns"),
    Input("save-button", "n_clicks"),
)
def save_data(
    table_data: list[dict[str, Any]],
    table_columns: list[dict[str, str]],
    *args: int,
) -> dict[str, str]:
    """Download the edited table to a geojson file.

    Parameters
    ----------
    table_data: list[dict]
        The data (taken from the table view box) of the table
        that should be displayed. This entry is needed to display any user
        modifications
    table_columns: list[str]
        The columns for the ``table_data```
    """
    if geo_json_obj.data_frame is None:
        raise exceptions.PreventUpdate
    data_frame = gp.GeoDataFrame(
        pd.DataFrame(table_data).astype(geo_json_obj.dtypes),
        geometry=geo_json_obj.data_frame["geometry"],
        crs=geo_json_obj.data_frame.crs,
    )
    with NamedTemporaryFile(suffix=".geojson") as temp_f:
        data_frame.to_file(temp_f.name, driver="GeoJSON")
        with open(temp_f.name, encoding="utf-8") as f_obj:
            content = f_obj.read()
    time = datetime.now().strftime("%Y%m%dT%H%M")
    out_file = f"geojsonviewer-{time}.geojson"
    return dict(content=content, filename=out_file)
