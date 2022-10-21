"""Collection of utilities to run and setup the geojson viewer app."""
from __future__ import annotations
import base64
from dataclasses import dataclass
import io
import logging
from pathlib import Path
from urllib.parse import urlparse
from typing import Any

import geopandas as gp
from dash import dash_table, html

logging.basicConfig(
    format="%(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("geojson-viewer")


@dataclass
class GeoJsonFile:
    """Class holding all information of the loaded geojson file.

    This class keeps track of the loaded geojson file and has methods
    that are able to modify/convert the data.

    Parameters
    ----------
    data_frame: str, default: None
        Ad pandas DataFrame representation of the geojson file.
    """

    data_frame: gp.geodataframe.GeoDataFrame | None = None

    def dash_data_table_from_dataframe(
        self, columns: list[str]
    ) -> list[dict[str, Any]]:
        """Convert the loaded geojson data to a dash_table format.

        Parameters
        ----------
        columns: list
            The name of the columns of the original geojson data that
            should be included.

        Returns
        -------
        list: Geojson data in dash_table format
        """

        out_table: list[dict[str, Any]] = []
        if self.data_frame is None:
            return out_table
        for line in self.data_frame[columns].values:
            out_table.append(dict(zip(columns, line)))
        return out_table

    @property
    def columns(self) -> list[str]:
        """Get all column names excpet geometry."""
        if self.data_frame is None:
            return []
        return [c for c in self.data_frame.columns if c != "geometry"]

    @property
    def dtypes(self) -> dict[str, type]:
        """Get the data types of each column."""
        if self.data_frame is None:
            return {}
        return {c: self.data_frame[c].dtype for c in self.columns}

    def to_viewbox(self) -> list[Any]:
        """Create the table div box that enables editing the geojson data.

        The method converts the geojson data to a data table and adds
        additional information and functionality ot the view box

        Returns
        -------
        list: A list of items that are displayed in the table editing view
              box.
        """
        if self.data_frame is None:
            return [
                html.P(
                    "Load geojson file in the display tab first",
                    style={"color": "red"},
                ),
                html.Br(),
                dash_table.DataTable(id="table"),
            ]
        columns = [c for c in self.data_frame.columns if c != "geometry"]
        return [
            html.P("To edit: click cells, adjust and press enter"),
            html.Br(),
            dash_table.DataTable(
                id="table",
                columns=[{"name": c, "id": c} for c in columns],
                data=self.dash_data_table_from_dataframe(columns),
                editable=True,
            ),
        ]


def load_geojson(
    inp_path: str | None, upload_content: str | None
) -> gp.geodataframe.GeoDataFrame:
    """Load a geojson file and return it's content.
    This method works for both, urls and files on disk.

    Parameters
    ----------
    inp_path: str, io.StringIO
        Path/buffer content of the resource

    Returns
    -------
    geopandas.geodataframe.GeoDataFrame: Loaded geopandas dataframe
    """
    content: str | io.StringIO = ""
    if inp_path is not None:
        content = inp_path.strip()
        parsed_url = urlparse(content)
        if not parsed_url.netloc and not parsed_url.scheme:
            # Assume this this is a path on the file system
            content = str(Path(content).expanduser().absolute())
    elif upload_content is not None:
        content = io.StringIO(read_upload_content(upload_content))
    return gp.read_file(content)


def read_upload_content(content: str) -> str:
    """Read upladed user content.

    Parameters
    ----------
    content: str
        The content string that is uploaded

    Returns
    -------
    str: The uploaded user content
    """
    _, content_string = content.split(",")
    return base64.b64decode(content_string).decode("utf-8")
