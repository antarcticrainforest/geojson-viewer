FROM condaforge/mambaforge:latest

ARG NB_USER="geoviewer"
ARG NB_UID="1000"

ENV USER=${NB_USER} \
    HOME=/tmp/${NB_USER} \
    NB_GID=${NB_UID} \
    NB_GROUP=${NB_USER} \
    DATA_FILES=/tmp/$NB_USER/.data

COPY . /tmp/clone

RUN set -e && \
  groupadd -r --gid "$NB_GID" "$NB_GROUP" && \
  adduser --uid "$NB_UID" --gid "$NB_GID" --gecos "Default user" \
  --shell /bin/bash --disabled-password "$NB_USER" --home $HOME && \
  mamba install -q -y dash geopandas gunicorn pandas &&\
  mamba run pip install /tmp/clone[jupyter] &&\
  cp /tmp/clone/Fallback.ipynb $HOME/ &&\
  rm -fr /tmp/clone &&\
  chown -R $NB_USER:$NB_GROUP $HOME

USER $NB_USER
WORKDIR $HOME
RUN set -e &&\
  mamba run python3 -m ipykernel install --name geojson-viewer --user
