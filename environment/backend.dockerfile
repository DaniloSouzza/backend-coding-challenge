FROM python:3.9.13-slim

RUN pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false

COPY dependencies/ .

RUN poetry install
RUN rm -r *.lock *.toml

WORKDIR /gistapi

COPY gistapi/ .
