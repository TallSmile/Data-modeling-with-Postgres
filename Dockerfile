FROM jupyter/base-notebook

RUN python --version

RUN pip install psycopg2-binary pandas ipython-sql

VOLUME /src
WORKDIR /src