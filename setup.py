from pathlib import Path
import re
from setuptools import setup, find_packages
from typing import List


def read(*parts: str) -> str:
    """Read the content of a file."""
    with Path(__file__).parent.joinpath(*parts).open() as f:
        return f.read()


def find_version(*parts: str) -> str:
    vers_file = read(*parts)
    match = re.search(r'^__version__ = "(\d+.\d+.\d+)"', vers_file, re.M)
    if match is not None:
        return match.group(1)
    raise RuntimeError("Unable to find version string.")


def get_assests(*parts: str) -> List[str]:
    asset_dir = Path(__file__).parent.joinpath(*parts)
    out = [str(d.relative_to(asset_dir.parent)) for d in asset_dir.rglob("*")]
    print(out)
    return out


meta = dict(
    description="View and manipulate geojson files",
    url="https://github.com/antarcticrainforest/geojson-viewer",
    author="Martin Bergemann",
    author_email="martin.bergemann@posteo.org",
    include_package_data=True,
    long_description_content_type="text/markdown",
    license="BSD-3-Clause",
    python_requires=">=3.7",
    package_data={"": get_assests("src", "geojson_viewer", "assets")},
    project_urls={
        "Issues": "https://github.com/antarcticrainforest/geojson-viewer/issues",
        "Source": "https://github.com/antarcticrainforest/geojson-viewer",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
    ],
    version=find_version("src", "geojson_viewer", "app.py"),
    package_dir={"": "src"},
    entry_points={"console_scripts": ["geojson-viewer = geojson_viewer.app:cli"]},
    install_requires=[
        "dash",
        "geopandas",
        "gunicorn",
        "pandas",
    ],
    extras_require={
        "tests": [
            "black",
            "flake8",
            "mypy",
        ],
        "jupyter": [
            "jupyter",
            "jupyterlab",
            "jupyter-dash",
        ],
    },
)

setup(name="geojson_viewer", packages=find_packages("src"), **meta)
