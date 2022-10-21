"""Main utilities for the geojson viewer."""

from __future__ import annotations
import argparse

from dash import Dash, dcc, html

from .layout import display_tab, edit_tab
from .server import app

__version__ = "2022.10.1"


def cli() -> None:
    """Construct the command line interface."""

    cli_app = argparse.ArgumentParser(
        prog="geojson-viewer",
        description="View and manipulate geojson files",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    cli_app.add_argument("--debug", action="store_true", default=False)
    cli_app.add_argument(
        "--port",
        type=int,
        default=8050,
        help="The port the app should be running on.",
    )
    cli_app.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )
    args = cli_app.parse_args()
    run_server(debug_mode=args.debug, port=args.port)


def run_server(
    debug_mode: bool = False, port: int = 8050, **kwargs: str
) -> None:
    """Set up and run the server serving the geojso viewer app.

    This server will serve a dash app running on localhost. Currently only
    the development mode of the server is supported.

    Parameters
    ----------
    debug_mode: bool, defautl: True
        Run server in debug mode.
    port: int, default: 5002
        The port the server application in running on.
    kwargs:
        Additional keyword arguments
    """
    app.layout = html.Div(
        children=[
            dcc.Tabs(
                [
                    dcc.Tab(
                        label="Display Geojson file",
                        children=[
                            html.Div(id="display", children=display_tab)
                        ],
                    ),
                    dcc.Tab(
                        label="Edit Geojson file",
                        children=[html.Div(id="edit", children=edit_tab)],
                    ),
                ]
            )
        ]
    )
    app.run_server(debug=debug_mode, port=str(port), **kwargs)
    return
