# Geojson viewer app

This is a small demo application using
[plotly's dash](https://dash.plotly.com/) framework. Dash was chosen
because it combines relatively simple and straight forward means for creating
interactive react.js web apps and is still able to fulfill the requirements
of this small application. Those requirements are:

[] Upload GeoJSON files, containing geo-referenced features and their properties.
[] Show uploaded features and their properties on a dynamic web map.
[] Modify existing properties for features shown on the map.
[] Save updated features with their properties to GeoJson file.

## Installation

### Pre-requisites

The application backend runs in a python environment, hence
[python](https://www.python.org) should be available on your computer.

### Using anaconda (recommended)
This application is best set up by is using a
dedicated [anaconda](https://www.anaconda.com/products/distribution)
environment. Hence it is strongly recommended to have anaconda installed
on the executing computer. All dependencies can be installed using the
following conda command:


```console
conda env create -q -n geoviewer python=3.10 -f environment.yml
```

Resolving dependencies can be quite slow. An alternative is using
[mamba](https://mamba.readthedocs.io/en/latest/user_guide/mamba.html)
instead of conda.

```console
mamba env create -q -n geoviewer python=3.10 -f environment.yml
```


### Using pip (virtualenv, pipenv etc)
If conda is not available you can directly install the dependencies via pip.
Still, it is recommended to use some kind of isolated python environment
for example provided by `virtualenv` or `pipenv`.

```
python -m pip install .
```

### Fallback
If the installation fails you can use a fallback binder instance. In this
instance the application is executed within a
[jupyter notebook](http://jupyter.org/) on binderhub. You can launch the server
by following this link
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/antarcticrainforest/geojson-viewer/main?labpath=Fallback.ipynb)

## Usage

To start the application use the following command:

```console
geojson-viewer --help
usage: geojson-viewer [-h] [--debug] [--port PORT] [-V]

View and manipulate geojson files

options:
  -h, --help     show this help message and exit
  --debug
  --port PORT    The port the app should be running on. (default: 8050)
  -V, --version  show program's version number and exit
```

For example the command:

```console
geojson-viewer --debug
```

will start the application in debug mode on port 8050. You can then open
the app via `http://localhost:8050/` on your browser.


## Sample data
Sample geojson data is provided in the repository (`montreal_elections.geojson`)
the same data can also be accessed via the following url:

[https://nextcloud.dkrz.de/s/keAxAjE5SMFQZ7C/download/montreal_elections.geojson](https://nextcloud.dkrz.de/s/keAxAjE5SMFQZ7C/download/montreal_elections.geojson)
